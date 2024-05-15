# lrclib-cli
A simple command line client for tranxuanthang's [LRCLIB](https://lrclib.net) lyrics hosting service, written in Python.

LRCLIB is a service by [@tranxuanthang](https://github.com/tranxuanthang) for hosting and scraping synced and non-synced lyrics for music, in the common [LRC](https://en.wikipedia.org/wiki/LRC_(file_format)) file format. I've found it super useful for downloading lyrics for any music I have stored on a Jellyfin server, however the only client is a graphical app designed for importing a library stored locally, which makes it less than ideal for my situation. So to solve my problem, I made this program!

lrclib-cli is a simple Python tool that reads the metadata of a music file and uses that to make a request to the LRCLIB API, and downloads synced lyrics if the song exists in the database and synced lyrics are available. If synced lyrics are not available, plain lyrics are downloaded instead.

lrclib-cli uses [Mutagen](https://github.com/quodlibet/mutagen) to parse the metadata of your music, so it should have support for music in any format that Mutagen can handle.

### Important:
For this tool to work properly, your music **must** have metadata tags for the title, artist, and album. These are all required parameters to use the LRCLIB API.

## Usage
```shell
python3 lrclib-cli.py <path to music file.mp3/.m4a/.whatever>
```

The script will inform you if either synced or plain lyrics were successfully downloaded (or if the song is an instrumental/lyrics aren't available), and the lyrics will be saved to an LRC file with the same name as your input file (minus the extension of course) in the same directory.
