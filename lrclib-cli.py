import os
import sys
import json

import mutagen
import requests


if __name__ == '__main__':
    try:
        in_file = sys.argv[1]
    except IndexError:
        print("You must pass in a file name!")
        exit(-1)
    if not os.path.isfile(in_file):
        raise FileNotFoundError(in_file)
    try:
        music_file = mutagen.File(in_file, easy=True)
    except mutagen.MutagenError:
        print("This does not appear to be a valid audio file!")
        exit(-1)
    try:
        track_artist = music_file["artist"][0]
        track_title = music_file["title"][0]
        track_album = music_file["album"][0]
        track_length = round(music_file.info.length)
    except KeyError:
        print("Audio metadata missing! This track could not be identified.")
        exit(-1)
    print("Track: " + music_file["title"][0] + "\nArtist: " + track_artist + "\nAlbum: " + track_album + "\nLength: " +
          str(track_length) + " seconds")
    lrclib_url = ("https://lrclib.net/api/get?" + "artist_name=" + track_artist + "&track_name=" + track_title +
                  "&album_name=" + track_album + "&duration=" + str(track_length))
    lrclib_response = requests.get(url=lrclib_url, stream=True)
    if lrclib_response.status_code == 200:
        lrclib_json = json.loads(lrclib_response.content)
        if lrclib_json["instrumental"] is False:
            with open(os.path.splitext(in_file)[0] + ".lrc", "w") as out_file:
                synced_lyrics = lrclib_json["syncedLyrics"]
                if synced_lyrics is None:
                    out_file.write(lrclib_json["plainLyrics"])
                    print("No synced lyrics available! Plain lyrics have been saved instead.")
                    exit(1)
                else:
                    out_file.write(synced_lyrics)
                    print("Synced lyrics have been saved!")
                    exit(0)
        else:
            print("This track is an instrumental!")
            exit(-2)
    elif lrclib_response.status_code == 404:
        print("No lyrics could be found for that track!")
        exit(-3)
    else:
        raise ConnectionError(lrclib_response)
