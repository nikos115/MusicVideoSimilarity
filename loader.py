import pandas as pd
from app import db
from app.models import Video, Meta


names = ['title',
         'artist',
         'folder', 'file', 'url',
         'genre',
         'danceability',
         'energy',
         'loudness',
         'speechness',
         'acousticness',
         'instrumentalness',
         'liveness',
         'valence',
         'tempo']

csv_df = pd.read_csv('../Music/metadata.csv', header=None, names=names)

# db.drop_all()
# db.create_all()

for row_index, row in csv_df.iterrows():
    metadata = Meta(title=row['title'],
                        artist=row['artist'],
                        genre=row['genre'],
                        danceability=row['danceability'],
                        energy=row['energy'],
                        loudness=row['loudness'],
                        speechness=row['speechness'],
                        acousticness=row['acousticness'],
                        instrumentalness=row['instrumentalness'],
                        liveness=row['liveness'],
                        valence=row['valence'],
                        tempo=row['tempo'])

    video = Video(directory=row['folder'], file=row['file']+'.mp4', url=row['url'], search=False, meta=[metadata])
    db.session.add(video)
    # Video.query.filter_by(url=row['url']).update(dict(directory=row['folder'], file=row['file']+'.mp4'))

db.session.commit()
