from app.models import Video, Segment, Feature, Encoding
from app import db
from sqlalchemy import func, desc
import os
import numpy as np
from keras.models import Model, load_model
from keras.layers import Input, LSTM, Dense, RepeatVector, TimeDistributed
from keras.utils import plot_model
from keras.callbacks import EarlyStopping
from keras import optimizers
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle


class Predictor:
    train_file = 'model/train.npz'
    composite_model_file = 'model/composite.h5'
    classifier_model_file = 'model/classifier.h5'
    encoder_model_file = 'model/encoder.h5'
    label_encoder_file = 'model/label_encoder.sav'
    scaler_file = 'model/scaler.sav'

    segment_no = 44
    feature_no = 422
    encoding_no = 40

    @staticmethod
    def get_x_y():
        if not os.path.isfile(Predictor.train_file):
            video_no = Video.query.filter_by(search=False).count()
            segment_no = db.session.query(func.count(Segment.video_id).label('cnt')).group_by(Segment.video_id).order_by(desc('cnt')).limit(1).scalar()
            feature_no = Feature.query.count()

            db_videos = Video.query.filter_by(search=False).order_by(Video.id).all()

            x = np.zeros([video_no, segment_no, feature_no])
            y = []
            ids = []
            i = 0

            for i in range(video_no):
                if not db_videos[i].segments:
                    continue

                video_ft = np.array([[ft.value for ft in segment.features] for segment in db_videos[i].segments])
                x[i, :video_ft.shape[0], :video_ft.shape[1]] = video_ft
                y.append(db_videos[i].genre)
                ids.append(db_videos[i].id)
                # i += 1
                db_videos[i] = None
                if i % 5 == 0:
                    print(i)

            y = np.array(y)
            ids = np.array(ids)

            np.savez_compressed(Predictor.train_file, x=x, y=y, ids=ids)

        else:
            file = np.load(Predictor.train_file)
            x = file['x']
            y = file['y']
            ids = file['ids']

        return x, y, ids

    @staticmethod
    def train():
        x, y, ids = Predictor.get_x_y()
        label_encoder = LabelBinarizer()
        y_encoded = label_encoder.fit_transform(y)
        pickle.dump(label_encoder, open(Predictor.label_encoder_file, 'wb'))

        x_train, x_val, y_train, y_val = train_test_split(x, y_encoded, test_size=0.10, stratify=y)

        # scale train, transform test
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train.reshape(-1, x_train.shape[-1])).reshape(x_train.shape)
        x_val = scaler.transform(x_val.reshape(-1, x_val.shape[-1])).reshape(x_val.shape)
        pickle.dump(scaler, open(Predictor.scaler_file, 'wb'))

        # define encoder
        visible = Input(shape=(x_train.shape[1], x_train.shape[2]))
        encoded = LSTM(Predictor.encoding_no, activation='relu', return_sequences=False, bias_initializer='lecun_uniform')(visible)
        # define reconstruct decoder
        decoded = RepeatVector(x_train.shape[1])(encoded)
        decoded = LSTM(Predictor.encoding_no, activation='relu', return_sequences=True, bias_initializer='lecun_uniform')(decoded)
        decoded = TimeDistributed(Dense(x_train.shape[2]), name='decode')(decoded)
        # define predict classifier
        classified = Dense(64, activation='relu')(encoded)
        # classified = Dense(20, activation='relu')(classified)
        classified = Dense(len(label_encoder.classes_), activation='softmax', name='classification')(classified)
        # tie it together
        compo = Model(inputs=visible, outputs=[decoded, classified])
        compo.compile(optimizer=optimizers.Adamax(), metrics=['accuracy'], loss=['mae', 'categorical_crossentropy'])
        compo.summary()
        plot_model(compo, show_shapes=True, to_file='model/composite.png')
        # fit model
        es = EarlyStopping(monitor='val_classification_accuracy', mode='max', verbose=0, patience=15, restore_best_weights=True)
        history = compo.fit(x_train, [x_train, y_train], validation_data=(x_val, [x_val, y_val]), epochs=150, batch_size=2, callbacks=[es])
        compo.save(Predictor.composite_model_file)
        scores = compo.evaluate(x_val, [x_val, y_val], verbose=0)

        plt.figure(figsize=(16, 5))

        # Plot training & validation accuracy values
        plt.subplot(1, 2, 1)
        plt.plot(history.history['decode_accuracy'])
        plt.plot(history.history['val_decode_accuracy'])
        plt.plot(history.history['classification_accuracy'])
        plt.plot(history.history['val_classification_accuracy'])
        plt.title('Model accuracy: ' + str(scores[1]))
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Decode Train', 'Decode Validation', 'Classification Train', 'Classification Validation'], loc='upper left')

        # Plot training & validation loss values
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.plot(history.history['decode_loss'])
        plt.plot(history.history['val_decode_loss'])
        plt.plot(history.history['classification_loss'])
        plt.plot(history.history['val_classification_loss'])
        plt.title('Model loss: ' + str(scores[0]))
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Validation', 'Decode Train', 'Decode Validation', 'Classification Train', 'Classification Validation'], loc='upper left')

        plt.tight_layout()
        plt.savefig('model/train_history.png')

        # save standalone models

        encoder = Model(inputs=visible, outputs=encoded)
        encoder.save(Predictor.encoder_model_file)

        classifier = Model(inputs=visible, outputs=classified)
        classifier.save(Predictor.classifier_model_file)

        # Plot confusion matrix heatmap
        y_pred = classifier.predict(x_val)
        # Convert from one hot encoding to a 2d matrix
        cm = confusion_matrix(y_val.argmax(axis=1), y_pred.argmax(axis=1))
        df_cm = pd.DataFrame(cm, index=label_encoder.classes_, columns=label_encoder.classes_)

        plt.figure(figsize=(10, 10))
        plt.xlabel('Predicted', fontsize=20)
        plt.ylabel('Actual', fontsize=20)

        sns.heatmap(df_cm, annot=True, fmt='g')
        plt.savefig('model/heatmap.png')

    @staticmethod
    def save_encodings(video_id):
        scaler = pickle.load(open(Predictor.scaler_file, 'rb'))
        label_encoder = pickle.load(open(Predictor.label_encoder_file, 'rb'))
        classifier = load_model(Predictor.classifier_model_file, compile=False)
        encoder = load_model(Predictor.encoder_model_file, compile=False)

        video = Video.query.filter_by(id=video_id).first()

        x = np.zeros([1, Predictor.segment_no, Predictor.feature_no])
        video_ft = np.array([[ft.value for ft in segment.features] for segment in video.segments])
        x[0, :video_ft.shape[0], :video_ft.shape[1]] = video_ft
        x = scaler.transform(x.reshape(-1, x.shape[-1])).reshape(x.shape)

        cls = classifier.predict(x)
        label = label_encoder.inverse_transform(cls)
        if video.search:
           video.genre = label[0]

        encodings = encoder.predict(x)
        encodings = encodings[0]

        # save to db
        video.encodings = [Encoding(video_id=video.id, seq_no=i + 1, value=encodings[i].astype(float)) for i in range(Predictor.encoding_no)]
        db.session.add(video)
        db.session.commit()


if __name__ == '__main__':
    p = Predictor()
    # p.train()
    db_videos = Video.query.all()
    for video in db_videos:
        if video.encodings:
            continue
        else:
            p.save_encodings(video.id)
