from download import Download

class Run:

    def __init__(self, genre, playlist, num_of_vid):

        self.genre = genre
        self.playlist = playlist
        self.num_of_vid = num_of_vid

    def run(self):
        Download(self.genre, self.playlist, self.num_of_vid).download()

#
# Add genre / playlist url / num of songs you want to download
#
Run('Metal','https://www.youtube.com/watch?v=xnKhsTXoKCI&list=PLhQCJTkrHOwSX8LUnIMgaTq3chP1tiTut',50).run()
