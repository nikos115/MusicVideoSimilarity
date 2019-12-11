from youtube import Youtube
import pytube
import sys
import spotipy
import spotipy.oauth2 as oauth2
import configparser
import os

class Spotify:

    def __init__(self, genre, num_of_vid):

        self.genre = genre
        self.num_of_vid = num_of_vid

        # spotify credentials
        config = configparser.ConfigParser()
        config.read('config.cfg')
        client_id = config.get('SPOTIFY', 'CLIENT_ID')
        client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
        auth = oauth2.SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        self.token = auth.get_access_token()

        #create genre folder
        self.dir = 'Music/'+self.genre
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def get_songs(self):

        spotify = spotipy.Spotify(auth=self.token)
        results = spotify.search(q=self.genre, type='playlist',limit=10)

        for playlist in results['playlists']['items']:

            if playlist['tracks']['total'] < self.num_of_vid:
                print('tracks less than '+ str(self.num_of_vid) + 'skipping to next playlist')
                continue

            else:
                playlist_tracks = spotify.user_playlist_tracks(playlist['owner']['id'], playlist['id'])
                print('playlist has ' +str(playlist_tracks['total'])+ ' songs.')

                f_cnt = -1
                s_cnt = 0
                for playlist_track in playlist_tracks['items']:

                    f_cnt += 1
                    if f_cnt == 0:
                        continue

                    try:
                        song_title = playlist_track['track']['artists'][0]['name'] + ' - ' + playlist_track['track']['name']
                        url = Youtube(song_title).search_video()
                        format = pytube.YouTube(url).streams.get_by_itag('133')

                        if s_cnt == self.num_of_vid:
                            break

                        s_cnt += 1
                        print('song: '+str(s_cnt)+ ': '+song_title+ ' | ' +url+ ' | ' +str(format))
                        format.download(self.dir)

                    except:
                        print('error. continuing to next song.')
                        continue

                break
