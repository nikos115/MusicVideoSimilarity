import threading
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from sqlalchemy import text
from app import app
from app import db
from app.forms import SearchForm, WeightForm
from app.models import Video, Meta
from pytube import YouTube
from processor import Processor
import os


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
                print(e)
                flash('Cannot download video. Please choose another.')

            else:
                video = Video(url=video_url, search=True)
                db.session.add(video)
                db.session.commit()

                # process video, extract features
                # threading.current_thread().setName('MainThread')
                p = Processor()
                p.process_file(yt.default_filename, video.id)
                os.remove(yt.default_filename)

        if video is not None:
            return redirect(url_for('search', video_id=video.id, features=form.features.data, distance=form.distance.data))

    searches = Video.query.filter_by(search=True).order_by(Video.id.desc()).limit(4).all()

    return render_template('index.html', title='Home', form=form, searches=searches)


@app.route('/search/<video_id>/<features>/<distance>')
def search(video_id, features='all', distance='l2'):
    video = Video.query.filter_by(id=video_id, search=True).first_or_404()

    # search
    sql = """
    SELECT haystack.id, haystack.url,
    (|/ (SUM ((haystacksegmentfeatures.value - needlesegmentfeatures.value) * weight) ^ 2)) as l2_distance,
    (SUM(haystacksegmentfeatures.value * needlesegmentfeatures.value * weight ^ 2) / ((|/ SUM(haystacksegmentfeatures.value * weight) ^ 2) * (|/ SUM(needlesegmentfeatures.value * weight) ^ 2))) as cosine_distance
    
    FROM video haystack
    INNER JOIN segment haystacksegment ON haystack.id = haystacksegment.video_id
    INNER JOIN segment_features haystacksegmentfeatures ON haystacksegment.id = haystacksegmentfeatures.segment_id
    
    INNER JOIN segment_features needlesegmentfeatures ON haystacksegmentfeatures.feature_id = needlesegmentfeatures.feature_id
    INNER JOIN segment needlesegment ON needlesegmentfeatures.segment_id = needlesegment.id
    INNER JOIN video needle ON needlesegment.video_id = needle.id AND needle.id != haystack.id AND needle.id = :id
    
    INNER JOIN feature ON haystacksegmentfeatures.feature_id = feature.id
    
    WHERE haystack.search = :search
    """
    if 'A' == features:
        sql += " AND feature.type='M'"
    elif 'V' == features:
        sql += " AND feature.type='V'"

    sql += " GROUP BY haystack.id, haystack.url, weight"

    if 'cos' == distance:
        sql += " ORDER BY cosine_distance"
    else:
        sql += " ORDER BY l2_distance"

    sql += " LIMIT 2"

    # results = db.session.execute(text(sql), id=video_id, search=False)

    results = db.session.query(Video).from_statement(text(sql)).params(id=video_id, search=False).all()
    print(results)

    searches = db.session.query(Video).from_statement(text(sql)).params(id=video_id, search=True).all()

    return render_template('search.html', title='Search Results', video=video, results=results, searches=searches)


@app.route('/weights', methods=['GET', 'POST'])
def weights():
    form = WeightForm()
    return render_template('weights.html', title='Weights', form=form)


@app.route('/genres', methods=['GET'])
def genres():
    genres = []
    for md in Meta.query.distinct(Meta.genre):
        genres.append(md.genre)
    return render_template('genres.html', title="Genres", genres=genres)


@app.route('/genre/<genre>')
def genre(genre):
    videos = db.session.query(Video).join(Meta).filter(Meta.genre == genre)
    return render_template('genre.html', title='Genre', videos=videos, genre=genre)

