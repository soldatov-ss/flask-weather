from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()], render_kw={"placeholder": "Enter a city name"})
    submit = SubmitField('Add')
