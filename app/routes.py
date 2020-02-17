from flask import render_template, flash, redirect, url_for
from sqlalchemy import text
from app import app
from app import db
from app.forms import SearchForm
from app.models import Video, Meta
from pytube import YouTube
from processor import Processor
from predictor import Predictor
import os
from collections import defaultdict
import urllib.parse
import matplotlib.pyplot as plt
import io
import base64


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        video_url = form.q.data

        # first check if the video is allready in database
        video = Video.query.filter_by(youtube_id=Video.get_youtube_id(video_url), search=True).first()
        if video is None:
            try:
                yt = YouTube(video_url).streams.filter(progressive=True).last()
                yt.download()

            except Exception as e:
                print(e, video_url)
                flash('Cannot download video. Please choose another.')

            else:
                video = Video(url=video_url, search=True)
                db.session.add(video)
                db.session.commit()

                # process video, extract features
                proc = Processor()
                proc.process_file(yt.default_filename, video.id)
                os.remove(yt.default_filename)

                pred = Predictor()
                pred.save_encodings(video.id)

        if video is not None:
            return redirect(url_for('search', video_id=video.id, ft=form.features.data, distance=form.distance.data))

    searches = Video.query.filter_by(search=True).order_by(Video.id.desc()).limit(4).all()

    return render_template('index.html', title='Home', form=form, searches=searches)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/search/<video_id>/<ft>/<distance>')
def search(video_id, ft, distance):
    video = Video.query.filter_by(id=video_id, search=True).first_or_404()

    # search

    sql = """
    SELECT haystack.id, haystack.url,
    (|/ (SUM ((haystacksegmentfeatures.value - needlesegmentfeatures.value) * weight) ^ 2)) as l2_distance,
    SUM((CASE WHEN haystack_sfl.length = 0 THEN 0 ELSE haystacksegmentfeatures.value / haystack_sfl.length END) * (CASE WHEN needle_sfl.length = 0 THEN 0 ELSE needlesegmentfeatures.value / needle_sfl.length END) * weight) as cosine_distance
    
    FROM video haystack
    INNER JOIN segment haystacksegment ON haystack.id = haystacksegment.video_id
    INNER JOIN segment_features haystacksegmentfeatures ON haystacksegment.id = haystacksegmentfeatures.segment_id
    INNER JOIN (
        SELECT |/ SUM(value ^ 2) as length, video_id, feature_id 
        FROM segment_features
        INNER JOIN segment ON segment_id = id
        GROUP BY video_id, feature_id
    ) haystack_sfl ON haystacksegment.video_id = haystack_sfl.video_id AND haystacksegmentfeatures.feature_id = haystack_sfl.feature_id
    
    INNER JOIN segment_features needlesegmentfeatures ON haystacksegmentfeatures.feature_id = needlesegmentfeatures.feature_id
    INNER JOIN segment needlesegment ON needlesegmentfeatures.segment_id = needlesegment.id
    INNER JOIN video needle ON needlesegment.video_id = needle.id AND needle.id != haystack.id AND needle.id = :id
    INNER JOIN (
        SELECT |/ SUM(value ^ 2) as length, video_id, feature_id 
        FROM segment_features
        INNER JOIN segment ON segment_id = id
        GROUP BY video_id, feature_id
    ) needle_sfl ON needlesegment.video_id = needle_sfl.video_id AND needlesegmentfeatures.feature_id = needle_sfl.feature_id
    
    INNER JOIN feature ON haystacksegmentfeatures.feature_id = feature.id
    
    WHERE haystack.search = :search
    """
    if 'A' == ft:
        sql += " AND feature.type='M'"
    elif 'V' == ft:
        sql += " AND feature.type='V'"
    elif 'E' == ft:
        sql = """
        SELECT haystack.id, haystack.url,
        (SUM(haystackencoding.value * needleencoding.value) / (|/ SUM((haystackencoding.value ) ^ 2 ) * |/ SUM((needleencoding.value) ^ 2))) as cosine_distance,
        (|/ (SUM(haystackencoding.value - needleencoding.value) ^ 2)) as l2_distance
        FROM video haystack
        INNER JOIN encoding haystackencoding ON haystack.id = haystackencoding.video_id
        INNER JOIN encoding needleencoding ON haystackencoding.seq_no = needleencoding.seq_no AND needleencoding.video_id != haystackencoding.video_id AND needleencoding.video_id = :id
        WHERE haystack.search = :search
        """

    sql += " GROUP BY haystack.id, haystack.url"

    if 'cos' == distance:
        sql += " ORDER BY cosine_distance DESC"
    else:
        sql += " ORDER BY l2_distance"

    sql += " LIMIT 4"

    results = db.session.query(Video).from_statement(text(sql)).params(id=video_id, search=False).all()

    searches = db.session.query(Video).from_statement(text(sql)).params(id=video_id, search=True).all()

    return render_template('search.html', title='Search Results', video=video, results=results, searches=searches)


@app.route('/genres', methods=['GET'])
def genres():
    genres = []
    for md in Video.query.distinct(Video.genre):
        genres.append(md.genre)
    return render_template('genres.html', title="Genres", genres=genres)


@app.route('/genre/<genre>')
def genre(genre):
    videos = db.session.query(Video).filter(Video.genre == genre)
    return render_template('genre.html', title='Genre', videos=videos, genre=genre)


@app.route('/features/<video_id>', methods=['GET'])
def features(video_id):
    video = Video.query.filter_by(id=video_id).first_or_404()
    segments = video.segments

    view_data = defaultdict(list)
    for segment in segments:
        view_data['SECONDS'].append(segment.start_sec)
        for sgf in segment.features:
            view_data[sgf.feature.description].append(sgf.value)
    img = io.BytesIO()  # create the buffer

    for k, v in view_data.items():
        if k in ['SECONDS', 'm', 's', 'mfcc_1_mean', 'energy_entropy_mean']:
            continue
        plt.plot(view_data['SECONDS'], v, label=k)

    plt.savefig(img, format='png')  # save figure to the buffer
    plt.close()
    img.seek(0)  # rewind your buffer

    plot_data = urllib.parse.quote(base64.b64encode(img.read()).decode())  # base64 encode & URL-escape

    return render_template('features.html', title='Video Features', video=video, data=view_data, plot_url=plot_data)
