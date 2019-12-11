import urllib.request
import urllib.parse
import re

class Youtube:

    def __init__(self, song_title):

        self.song_title = song_title

    def search_video(self):

        query_string = urllib.parse.urlencode({"search_query" : self.song_title})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        if search_results[0] != '':
            return "http://www.youtube.com/watch?v=" + search_results[0]
        else:
            return ''

    '''
    def get_video_urls(self):

        page = requests.get(self.playlist)
        soup = BeautifulSoup(page.text, 'html.parser')

        videos = set()
        for a in soup.find_all('a'):
            if a.get('href').startswith('/watch'):
                videos.add('https://youtube.com' + a.get('href').split('&')[0])

        return videos





        videos = self.get_video_urls()

        if not os.path.exists(dir):
            os.makedirs(dir)

        cnt=1
        for video in videos:

            #try:

            title = pytube.YouTube(video).title

            # get metadata from spotify
            Metas(title).get_metas()
            break

            #format = pytube.YouTube(video).streams.get_by_itag('133')
            #print(title)
            #print(format)



            #except:

                #print('exception')
                #continue


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
            '''
