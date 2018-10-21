#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

from util import *
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyWrapper(object):

    def __init__(self, client_creds, albums):

        client_creds = SpotifyClientCredentials(*client_creds)
        self.spotify = Spotify(client_credentials_manager=client_creds)
        self.spotify.trace = False

        self.albums = albums
        self.table = []
        self.MAX_ALBUMS = 20
        self.MAX_AUDIO_FEATS = 100

    def get_album_uri(self):

        for album_ix, album in enumerate(self.albums):
            resp = self.spotify.search(
                q="album:{} artist:{}".format(*album), type="album", limit=10
            )

            if resp["albums"]["total"]:
                self.table.append(
                    (album + (resp["albums"]["items"][0]
                              ["uri"].replace("spotify:album:", ''), ))
                )

            else:
                # self.table.append((album + (None, )))
                wprint("No response for:", album)

    def get_tracklist_uris(self):

        tracklists = []

        # increment by MAX_ALBUMS album IDs
        for album_ix in range(0, len(self.table), self.MAX_ALBUMS):
            resp = self.spotify.albums(
                [
                    album[2] for album in
                    self.table[album_ix:album_ix + self.MAX_ALBUMS] if album[2]
                ]
            )
            # append all the responses
            tracklists.append(resp)

        # sometimes more than a page is returned
        for resp in tracklists:
            for group_ix in range(len(resp["albums"])):
                self.table[group_ix] = (
                    self.table[group_ix] + (",".join(
                        tracks["uri"].replace("spotify:track:", '')
                        for tracks in
                        resp["albums"][group_ix]["tracks"]["items"]
                    ),)
                )

    def get_table(self):

        return self.table
