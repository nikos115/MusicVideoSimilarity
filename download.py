import os
import requests
import pytube
from bs4 import BeautifulSoup

class Download:

    def __init__(self, genre, playlist, num_of_vid):

        self.genre = genre
        self.playlist = playlist
        self.num_of_vid = num_of_vid

    def get_video_urls(self):

        page = requests.get(self.playlist)
        soup = BeautifulSoup(page.text, 'html.parser')

        videos = set()
        for a in soup.find_all('a'):
            if a.get('href').startswith('/watch'):
                videos.add('https://youtube.com' + a.get('href').split('&')[0])

        return videos

    def download(self):

        dir = 'Music/'+self.genre

        videos = self.get_video_urls()

        if not os.path.exists(dir):
            os.makedirs(dir)

        cnt=1
        for video in videos:

            try:
                pytube.YouTube(video).streams.first().download(dir)
                print( video + ' Video '+str(cnt)+ ' Downloaded')
                cnt+=1
                if cnt == self.num_of_vid:
                    print( str(cnt)+' Songs Of '+self.genre+' Downloaded in /'+dir )
                    break
            except:
                print('exception')
                continue
