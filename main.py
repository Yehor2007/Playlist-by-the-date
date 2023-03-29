
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = os.environ('CLIENT_ID')
CLIENT_SECRET = os.environ('CLIENT_SECRET')
URI = 'http://example.com'
url_endpoint = 'https://api.spotify.com/v1/search'



date = input('Which year do you want to travel to? Type date in this format YYYY-MM-DD. ')
year = int(date.split('-')[0])

url = f'https://www.billboard.com/charts/hot-100/{date}'
response = requests.get(url=url)
response.raise_for_status()

content = response.text

soup = BeautifulSoup(content, "html.parser")

first_song = soup.find(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet").getText().strip()
first_singer = soup.find(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet").getText().strip()

top_100 = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
top_100_singers = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
top_100 = [song.getText().strip() for song in top_100]
top_100_singers = [song.getText().strip() for song in top_100_singers]
top_100.insert(0, first_song)
top_100_singers.insert(0, first_singer)





sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET, redirect_uri=URI, scope="playlist-modify-private"))
user_id = sp.current_user()["id"]
song_uris = []
for track in top_100:
    data = sp.search(q=f"track: {track} year: {year}", type='track')
    try:
        uri = data["tracks"]["items"][0]["uri"]
        print(uri)
        song_uris.append(uri)
    except IndexError:
        print(f"{track} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, public=False, name=f'{date} Billboard 100')
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)




