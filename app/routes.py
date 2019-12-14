from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from sqlalchemy import text
from app import app
from app import db
from app.forms import SearchForm
from app.models import Video

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        video_url = form.q.data
        # first check if the video is allready in database
        video = Video.query.filter_by(url=video_url, search=True).first()
        if video is None:
            video = Video(url=video_url, search=True)
            db.session.add(video)
            db.session.commit()

            # process video, extract features

        return redirect(url_for('search', video_id=video.id))

    searches = Video.query.filter_by(search=True).order_by(Video.id.desc()).limit(4).all()

    return render_template('index.html', title='Home', form=form, searches=searches)


@app.route('/search/<video_id>')
def search(video_id):
    video = Video.query.filter_by(id=video_id, search=True).first_or_404()

    # search
    sql = """
    SELECT haystack.id, haystack.url,
    (|/ (SUM (haystacksegmentfeatures.value - needlesegmentfeatures.value) ^ 2)) as l2_distance,
    ((SUM(haystacksegmentfeatures.value * needlesegmentfeatures.value)) / ((|/ SUM(haystacksegmentfeatures.value) ^ 2) * (|/ SUM(needlesegmentfeatures.value) ^ 2))) as cosine_distance
    
    FROM video haystack
    INNER JOIN segment haystacksegment ON haystack.id = haystacksegment.video_id
    INNER JOIN segment_features haystacksegmentfeatures ON haystacksegment.id = haystacksegmentfeatures.segment_id
    
    INNER JOIN segment_features needlesegmentfeatures ON haystacksegmentfeatures.feature_id = needlesegmentfeatures.feature_id
    INNER JOIN segment needlesegment ON needlesegmentfeatures.segment_id = needlesegment.id
    INNER JOIN video needle ON needlesegment.video_id = needle.id AND needle.id != haystack.id AND needle.id = :id
    
    where haystack.search = :search
    
    GROUP BY haystack.id, haystack.url
    
    ORDER BY l2_distance
    """

    # results = db.session.execute(text(sql), id=video_id, search=False)

    results = db.session.query(Video).from_statement(text(sql)).params(id=video_id, search=False).all()

    return render_template('search.html', title='Search Results', video=video, results=results)


@app.route('/weights', methods=['GET', 'POST'])
def weights():
    pass
