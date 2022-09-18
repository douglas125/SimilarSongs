from flask import Flask
from flask import url_for
from flask import request
from flask import render_template

from utils import read_songs

app = Flask(__name__, static_folder="videos")


@app.route("/")
def main_page():
    # flask --app similarsongs --debug run
    song_files = read_songs.get_song_files()
    song_urls = [url_for("song", songname=x) for x in song_files]
    local_song_urls = [url_for("localsong", songname=x) for x in song_files]

    return render_template(
        "index.html",
        name="Similar song browser",
        navigation=zip(song_urls, song_files, local_song_urls),
    )


@app.route("/song")  # , methods=['GET', 'POST'])
def song():
    songname = request.args.get("songname")
    songlist = read_songs.get_song_info(songname)
    if songlist is not None:
        return render_template(
            "songlist.html",
            songname=songname,
            songlist=songlist,
        )
    else:
        return f"{songname} not found!", 400


@app.route("/localsong")  # , methods=['GET', 'POST'])
def localsong():
    songname = request.args.get("songname")
    songlist = read_songs.get_local_names(songname)
    for s in songlist:
        s["local_name"] = url_for("static", filename=s["local_name"])

    if songlist is not None:
        return render_template(
            "localsonglist.html",
            songname=songname,
            songlist=songlist,
        )
    else:
        return f"{songname} not found!", 400
