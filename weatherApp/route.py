from datetime import datetime

import requests
from flask import request, render_template, flash, redirect, url_for

from weatherApp import app, db
from weatherApp.forms import CityForm
from weatherApp.models import Cities


def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': '',  # <--WRITE YOUR TOKEN FROM OPENWEATHERMAP :)
        'units': 'metric'
    }
    city_temp = requests.get(url, params=params)

    try:
        weather_type = city_temp.json()['weather'][0]['main']
        temp = city_temp.json()['main']['temp']
        return [int(temp), weather_type]
    except KeyError:
        flash("The city doesn't exist!", "danger")
        return None


def get_weather_in_4_hours(city):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'appid': '',  # <--WRITE YOUR TOKEN FROM OPENWEATHERMAP :)
        'units': 'metric',
        'cnt': 5
    }
    city_temp = requests.get(url, params=params)
    result_request = city_temp.json()['list']
    result = []

    for i in range(1, 5):
        time = datetime.strptime(result_request[i]['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
        temp = int(result_request[i]['main']['temp'])
        weather_type = result_request[i]['weather'][0]['main']

        result.append([time, temp, weather_type])

    return result


@app.route('/', methods=['POST', 'GET'])
def index():
    form = CityForm()
    cities = Cities.query.all()
    if form.validate_on_submit():
        if not get_weather(form.city.data):
            return redirect(url_for('index'))

        city_in = Cities.query.filter_by(city_name=form.city.data.upper()).first()

        if city_in:
            flash('The city has already been added to the list!', 'danger')
            return redirect(url_for('index'))

        city = Cities(city_name=form.city.data.upper())
        db.session.add(city)
        db.session.commit()
        flash('Your city has been added!', 'success')
        return redirect(url_for('index'))

    elif request.method == 'GET':
        weather_now, weather_in_4_hours = {}, {}
        for item in cities:
            weather_now[item] = get_weather(item.city_name)
            weather_in_4_hours[item] = get_weather_in_4_hours(item.city_name)

        return render_template('index.html', cities=cities, form=form,
                               weather_now=weather_now, weather_in_4_hours=weather_in_4_hours)
    return render_template('index.html', cities=cities, form=form)


@app.post('/delete/<int:city_id>')
def delete(city_id):
    city = Cities.query.get(city_id)
    db.session.delete(city)
    db.session.commit()
    flash('Your city has been deleted!', 'success')
    return redirect(url_for('index'))
