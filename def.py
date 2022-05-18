import requests
import webbrowser
import base64
import json

#Declarationof important variables

refresh_token = None
client_id = ""
client_secret = ""
clientc = f"{client_id}:{client_secret}"
b64 = base64.b64encode(clientc.encode()).decode()
redirect_uri = "http://localhost/"



def auth(client_id,redirect_uri):
    url = "https://accounts.spotify.com/authorize"
    # getting code after opening webbrowser
    webbrowser.open(url + f"?client_id={client_id}&scope=user-read-currently-playing user-read-playback-state&response_type=code&redirect_uri={redirect_uri}")
    code = input("Enter the code")[23:]
    return code


def access_token():

    code = auth(client_id,redirect_uri)
    # API TOKEN
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Authorization": f"Basic {b64}"
    }
    x = requests.post(url, data=payload, headers=headers)
    print(x.json())
    with open("tokens.json", 'w') as outfile:
        json.dump(x.json(), outfile)


def getsong():
    file = open("tokens.json", "r")
    x = json.loads(file.read())
    file.close()
    access_token = x['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    r = requests.get(url, headers=headers)

    js = r.json()
    artist_name = js['item']['album']['artists'][0]['name']
    song_name =  js['item']['name']
    print(artist_name, song_name, sep=', ')
getsong()
