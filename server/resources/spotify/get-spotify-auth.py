import spotipy.util as util

token = util.prompt_for_user_token('your-username',
                           'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-library-read user-read-currently-playing',
                           client_id='',
                           client_secret='',
                           redirect_uri='https://oskar.pw/',
                           cache_path='spotify-auth')

print("\nToken: ", token)
