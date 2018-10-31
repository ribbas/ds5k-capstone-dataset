
def aggregate_reviews():
    """
    subquery =
    SELECT
        TRIM(am.album), TRIM(am.artist),
        am.genre, mc.genre, pf.genre,
        am.time, mc.time, pf.time,
        am.score, mc.score, pf.score,
        am.reviewer, mc.reviewer, pf.reviewer
        FROM allmusic AS am
        INNER JOIN metacritic AS mc ON am.album = mc.album
        INNER JOIN pitchfork AS pf ON am.album = pf.album
        WHERE (
            TRIM(am.album) == TRIM(pf.album) AND
            TRIM(am.album) == TRIM(mc.album) AND
            TRIM(am.artist) == TRIM(pf.artist) AND
            TRIM(am.artist) == TRIM(mc.artist)
        );
    """

    db = DataBase(DB_PATH)
    tables = ("allmusic", "metacritic", "pitchfork")
    cond = ("TRIM(allmusic.album) == TRIM(pitchfork.album) AND "
            "TRIM(allmusic.album) == TRIM(metacritic.album) AND "
            "TRIM(allmusic.artist) == TRIM(pitchfork.artist) AND "
            "TRIM(allmusic.artist) == TRIM(metacritic.artist) COLLATE NOCASE")
    kind = "INNER"
    fields = [
        "TRIM(allmusic.album) as album",
        "TRIM(allmusic.artist) as artist",
        "allmusic.genre AS am_genre",
        "metacritic.genre AS mc_genre",
        "pitchfork.genre AS pf_genre",
        "allmusic.time AS am_time",
        "metacritic.time AS mc_time",
        "pitchfork.time AS pf_time",
        "allmusic.score AS am_score",
        "metacritic.score AS mc_score",
        "pitchfork.score AS pf_score",
        "allmusic.reviewer AS am_reviewer",
        "metacritic.reviewer AS mc_reviewer",
        "pitchfork.reviewer AS pf_reviewer"
    ]
    super_fields = [
        "album",
        "artist",
        "am_genre",
        "mc_genre",
        "pf_genre",
        "am_time",
        "mc_time",
        "pf_time",
        "AVG(am_score)",
        "AVG(mc_score)",
        "AVG(pf_score)",
        "am_reviewer",
        "mc_reviewer",
        "pf_reviewer",
    ]
    join_col = "album"
    groupby_cols = ("album", "artist")
    joins = (
        "{kind} JOIN {sub} ON {main}.{col} = {sub}.{col} ".format(
            kind=kind, main=tables[0], sub=t, col=join_col)
        for t in tables[1:]
    )
    q = "SELECT {sup_fields} FROM (SELECT {fields} FROM {main} {joins}WHERE ({cond})) GROUP BY {groupby_cols}".format(
        sup_fields=", ".join(super_fields),
        fields=", ".join(fields),
        main=tables[0],
        joins="".join(joins),
        cond=cond,
        groupby_cols=", ".join(groupby_cols)
    )

    join_dump = db.query(q)

    db.create("reviews", REVIEW_FIELDS)
    db.create("genres", GENRE_FIELDS)

    review_rows = []
    genre_rows = []
    for row in join_dump:
        # row[0:2] := album, artist
        # row[2:5] := genres
        # row[5:8] := dates
        # row[8:11] := scores
        # row[11:] := reviewers

        genre_row = get_genres(row[2:5])
        agg_row = (*row[0:2], get_earliest_date(row[5:8]), *normalize_scores(
            row[8:11], [5, 100, 10]), get_reviewers(row[11:]))
        review_rows.append(agg_row)
        genre_rows.append(genre_row)

    db.insert("reviews", review_rows, REVIEW_FIELDS)
    db.insert("genres", genre_rows, GENRE_FIELDS)
