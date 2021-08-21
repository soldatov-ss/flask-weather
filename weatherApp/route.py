from datetime import datetime

import aiohttp
from flask import request, render_template, flash, redirect, url_for

from weatherApp import app, db
from weatherApp.forms import CityForm
from weatherApp.models import Cities


async def get(url: str, city: str, cnt: int = None):
    if cnt:
        params = {
            'q': city,
            'appid': '',  # <--WRITE YOUR TOKEN FROM OPENWEATHERMAP :)
            'units': 'metric',
            'cnt': cnt
        }
    else:
        params = {
            'q': city,
            'appid': '',
            'units': 'metric',
        }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            res = await response.json()
            return res


async def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city_temp = await get(url, city)
    try:
        weather_type = city_temp['weather'][0]['main']
        temp = city_temp['main']['temp']
        return [int(temp), weather_type]
    except KeyError:
        flash("The city doesn't exist!", "danger")
        return None


async def get_weather_in_4_hours(city):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    city_temp = await get(url, city=city, cnt=5)
    result_request = city_temp['list']
    result = []

    for i in range(1, 5):
        time = datetime.strptime(result_request[i]['dt_txt'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
        temp = int(result_request[i]['main']['temp'])
        weather_type = result_request[i]['weather'][0]['main']

        result.append([time, temp, weather_type])

    return result


@app.route('/', methods=['POST', 'GET'])
async def index():
    form = CityForm()
    cities = Cities.query.all()
    if form.validate_on_submit():
        if not await get_weather(form.city.data):
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
            weather_now[item] = await get_weather(item.city_name)
            weather_in_4_hours[item] = await get_weather_in_4_hours(city=item.city_name)
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
