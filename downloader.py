from pytube import YouTube

class Downloader:

    def __init__(self):

        #self.path = "/media/sf_data_science/multimodal/MusicVideoSimilarity/"
        self.link = "https://www.youtube.com/watch?v=3gK_2XdjOdY"

    def download(self):
        
        YouTube(self.link).streams.first().download()


dl = Downloader()
dl.download()
