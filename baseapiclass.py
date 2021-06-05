import requests
import base64
import datetime

client_id, client_secret = "a10c32b0e8874c7e90984cb15053dbc1", "1cb585f9b30a486da168170f2d8183b9"


class SpotifyAPI(object):
    access_token = None
    access_token_expires = None
    client_id = "a10c32b0e8874c7e90984cb15053dbc1"
    client_secret = "1cb585f9b30a486da168170f2d8183b9"
    access_token_did_expire = True

    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None:
            print("Your must set client id and clint sercret")

        client_creds = f"{client_id}:{client_secret}"
        client_creds_64 = base64.b64encode(client_creds.encode())
        return client_creds_64.decode()  # decode from b to str

    def get_token_header(self):
        client_creds_64 = self.get_client_credentials()
        return {"Authorization": f"Basic {client_creds_64}"}

    def get_token_data(self):
        return {
            "grant_type": "client_credentials",
            "code" : "AQC6YiiKOkqvaeNGT8-pVewIGC_Y8yuI0fcajgPD6KiD6Nq9QPY8s8k9XekpeWkvtIvIBns9d4T3vlYf6t8RuNE6lPQ7NfnH2kE7LYVrgey3bVsrIaQIWnFqv6lBgHRQap0RHtr38iVVHddEBhHYmFRQNkgTdwD_7b59HtgBoHUEEA-3Vl3RbwWpBWXa8X5s9_k"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)

        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True


spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access = spotify.access_token
print(access)
url = "https://api.spotify.com/v1/me/player/currently-playing"



tokenheader=  {
    'Authorization': 'Bearer ' + access
}
print (access)

r = requests.get("https://api.spotify.com/v1//player/currently-playing", headers=tokenheader)
print(r.json())