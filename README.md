# ds5k-capstone

Dataset for DS5K capstone

## Tables

### album_df 
Maps album IDs to album and artist names

__Features__
- `album_id`: ID of album
- `album`: name of the album
- `artist`: name of the album's artist

### feat_df
Maps album IDs to their [Spotify audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/). The audio features are obtained on track-level and are therefore normalized to albums.

__Features__
- `album_id`: IDs of the album
- `explicit`: percentage of explicit tracks in album
- `tracks_count`: number of tracks in album

_The following features, with the exception of the boolean `mode`, are represented as the mean, median, minimum and maximum per the albums_
- `duration_ms`: Duration of tracks
- `danceability`: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- `energy`: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- `key`: The key the track is in. Integers map to pitches using standard [Pitch Class notation](https://en.wikipedia.org/wiki/Pitch_class). E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
- `loudness`: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.
- `mode`: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
- `speechiness`: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- `acousticness`: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
- `instrumentalness`: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- `liveness`: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- `valence`: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
- `tempo`: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
- `time_signature`: An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).

### review_df and genre_df
Maps album IDs to the scraped reviews data.

The reviews data are scraped from:
- AllMusic
- Metacritic
- Pitchfork

__Features__
- `album_id`: IDs of the album
- `time`: average time of reviews' publications
- `allmusic`: AllMusic score (out of 100)
- `metacritic`: Metacritic score (out of 100)
- `pitchfork`: Pitchfork score (out of 100)
- `score_mean`: Mean of the scores from all the reviewers
- `score_std`: Standard deviation of the score from all the reviewers
- `reviewers`: Authors of the reviews

_The following features are represented as a binary vector, where 1 represents presence of influences of the genre in the album_

|country|classical|electronic|experimental|folk|hiphop|international|jazz|metal|pop|rock|
|-------|---------|----------|------------|----|------|-------------|----|-----|---|----|
