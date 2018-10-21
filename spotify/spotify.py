#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import *
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyWrapper(object):

    def __init__(self, client_creds, albums):

        iprint("Setting up Spotify client")
        self.sp = Spotify(
            client_credentials_manager=SpotifyClientCredentials(*client_creds))
        self.sp.trace = False

        # Sqpotify API endpoint limits
        self.MAX_ALBUMS = 20
        self.MAX_AUDIO_FEATS = 100
        self.MAX_SEARCH = 50

        self.albums = albums
        self.table = []

    def get_table(self):

        return self.table

    def get_albums_uris(self):

        iprint("Getting album URIs")
        for album_ix, album in enumerate(self.albums):
            resp = self.sp.search(
                q="album:{} artist:{}".format(*album), type="album",
                limit=self.MAX_SEARCH
            )

            if resp["albums"]["total"]:
                self.table.append(
                    (album + (resp["albums"]["items"][0]
                              ["uri"].replace("spotify:album:", ''), ))
                )
                sprint("Received response for:", " by ".join(album))

            else:
                wprint("No response for:", " by ".join(album))

    def get_tracklists_uris(self):

        tracklists = []

        iprint("Getting tracks URIs")
        # increment by MAX_ALBUMS album IDs
        for album_ix in range(0, len(self.table), self.MAX_ALBUMS):
            resp = self.sp.albums(
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

    def get_tracks_analysis(self):

        pass
