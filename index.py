from spotify import Spotify

class Index:

    def __init__(self, genre, num_of_vid):

        self.genre = genre
        self.num_of_vid = num_of_vid

    def run(self):
        Spotify(self.genre, self.num_of_vid).get_songs()

# Add genre / num of songs you want to download
Index('Metal',60).run()
