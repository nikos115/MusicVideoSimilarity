from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


class SearchForm(FlaskForm):
    q = StringField(validators=[DataRequired(), URL()], render_kw={"placeholder": "Enter video URL"})
    features = SelectField('Features', validators=[DataRequired()], choices=[('E', 'NN Encodings'), ('V', 'Video only'), ('A', 'Audio only'), ('B', 'Both Audio and Video')], default='E')
    distance = SelectField('Distance metric', validators=[DataRequired()], choices=[('l2', 'Euclidian'), ('cos', 'Cosine Similarity')], default='l2')
    submit = SubmitField('Search')
