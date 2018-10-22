#!/usr/bin/env python
# -*- coding: utf-8 -*-

from statistics import mean, median

from util import *
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

FEATS = (
    "duration_ms",
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature"
)


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
                    self.table[group_ix] + (
                        ",".join(  # comma joined URIs
                            tracks["uri"].replace("spotify:track:", '')
                            for tracks in
                            resp["albums"][group_ix]["tracks"]["items"]
                        ), mean(  # percentage of explicit tracks
                            tracks["explicit"] for tracks in
                            resp["albums"][group_ix]["tracks"]["items"]
                        )
                    )
                )

    def __stats(self, feats):

        stats = []
        for attr in FEATS:
            stats.append(mean(resp[attr] for resp in feats))
            stats.append(median(resp[attr] for resp in feats))
            stats.append(min(resp[attr] for resp in feats))
            stats.append(max(resp[attr] for resp in feats))

        return tuple(stats)

    def get_tracks_analysis(self):

        iprint("Getting audio analysis on tracks")
        track_uris = ",".join(i[4] for i in self.albums).split(",")

        feats = []
        for uri_ix in range(0, len(track_uris), self.MAX_AUDIO_FEATS):
            feats.extend(self.sp.audio_features(
                track_uris[uri_ix:uri_ix + self.MAX_AUDIO_FEATS]))

        uri_ix = 0
        for album_ix in range(len(self.albums)):
            n_albums = self.albums[album_ix][4].count(",") + 1
            self.table.append(self.__stats(feats[uri_ix:uri_ix + n_albums]))
            uri_ix += n_albums
