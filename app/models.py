from app import db
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    type = db.Column(db.String(1), nullable=False)
    weight = db.Column(db.Float(), nullable=False)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(160), nullable=False)
    search = db.Column(db.Boolean, nullable=False, index=True)
    genre = db.Column(db.String(64))
    directory = db.Column(db.String(250))
    file = db.Column(db.String(250))
    youtube_id = db.Column(db.String(64))

    segments = db.relationship('Segment', lazy='select', backref=db.backref('video', lazy='joined'))
    meta = db.relationship('Meta', lazy='joined', backref=db.backref('video', lazy='joined'))
    encodings = db.relationship('Encoding', lazy='select', backref=db.backref('video', lazy='joined'))

    @staticmethod
    def get_youtube_id(url):
        return url.replace('http://', '').replace('https://', '').replace('www.youtube.com/watch?v=', '').replace('youtu.be/', '')

    def __init__(self, **kwargs):
        super(Video, self).__init__(**kwargs)
        self.youtube_id = Video.get_youtube_id(self.url)

    def __repr__(self):
        return '<Video id:{} youtube_id:{}, search:{}>'.format(self.id, self.youtube_id, self.search)


class Segment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), index=True)
    start_sec = db.Column(db.SmallInteger)
    end_sec = db.Column(db.SmallInteger)

    features = db.relationship('SegmentFeatures', lazy='joined', backref=db.backref('segment', lazy='joined'))


class SegmentFeatures(db.Model):
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'), primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    seq_no = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)

    feature = db.relationship('Feature', lazy='joined')


class Encoding(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    seq_no = db.Column(db.Integer, primary_key=True)
    value = db.Column(DOUBLE_PRECISION)


class Meta(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    artist = db.Column(db.String(160), nullable=False)
    # genre = db.Column(db.String(160), nullable=False)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    loudness = db.Column(db.Float)
    speechness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
