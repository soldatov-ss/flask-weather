from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class CityForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()],  render_kw={"placeholder": "Enter a city name"})
    submit = SubmitField('Add')

    # def check_in_db(self, city):
    #     city_in = CitiesWeather.query.filter_by(city_name=city).first()
    #     if city_in:
    #         raise ValidationError('The city has already been added to the list!')
