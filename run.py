from read import Read
from song import Song

class Run:

    def run(self):

        labels = Read('music_genres.csv').read_csv();
        Song(labels).check_songs(60);

Run().run()
