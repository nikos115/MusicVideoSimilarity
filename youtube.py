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
