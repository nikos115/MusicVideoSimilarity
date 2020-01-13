import pandas as pd
from app import db
from app.models import Video, Metadata


names = ['title', 'artist', 'path', 'url',
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

csv_df = pd.read_csv('Music/metadata.csv', header=None, names=names)

for row_index, row in csv_df.iterrows():
    metadata = Metadata(title=row['title'],
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
    print(metadata)
