from pytube import YouTube

class Download:

    def __init__(self,link):

        self.link = link

    def download(self):

        YouTube(self.link).streams.first().download()

link = "https://www.youtube.com/watch?v=3gK_2XdjOdY"

dl = Download(link)
dl.download()
