from app import db


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    type = db.Column(db.String(1), nullable=False)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(160), nullable=False)
    search = db.Column(db.Boolean, nullable=False)
    file = db.Column(db.String(250))

    segments = db.relationship('Segment', lazy='select', backref=db.backref('video', lazy='joined'))
    meta = db.relationship('Metadata', lazy='select', backref=db.backref('video', lazy='joined'))

    def youtube_id(self):
        return self.url.replace('https://www.youtube.com/watch?v=', '')


class Segment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), index=True)
    start_sec = db.Column(db.SmallInteger)
    end_sec = db.Column(db.SmallInteger)

    features = db.relationship('SegmentFeatures', lazy='select', backref=db.backref('segment', lazy='joined'))


class SegmentFeatures(db.Model):
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id'), primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'), primary_key=True)
    value = db.Column(db.Float)

    feature = db.relationship('Feature', lazy='joined')


class Metadata(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    artist = db.Column(db.String(160), nullable=False)
    genre = db.Column(db.String(160), nullable=False)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    loudness = db.Column(db.Float)
    speechness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
