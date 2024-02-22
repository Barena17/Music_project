from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)  # Change the path to your templates folder.

SPOTIFY_CLIENT_ID = "71e8abde29ae4664b795ecf51e9fda1d"
SPOTIFY_CLIENT_SECRET = "2ea2d2228faf4c30bde804029b8e638a"

# Function to get access token from Spotify
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {auth_b64}"}
    payload = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=payload)
    return response.json()["access_token"]

# Function to search Spotify for tracks or artists
def search_spotify(query, token, search_type):
    url = f"https://api.spotify.com/v1/search?q={query}&type={search_type}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        search_type = request.form["search_type"]
        token = get_access_token()
        results = search_spotify(query, token, search_type)
        if search_type == "track":
            return render_template("track_info.html", results=results, query=query)
        elif search_type == "artist":
            return render_template("artist_info.html", results=results, query=query)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)