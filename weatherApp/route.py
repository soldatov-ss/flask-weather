from weatherApp import app, db
import requests
from flask import request, render_template, flash, redirect, url_for
from weatherApp.models import Cities
from weatherApp.forms import CityForm


def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': f'{city}',
        'appid': '',               # <--WRITE YOUR TOKEN FROM OPENWEATHERMAP :)
        'units': 'metric'
    }
    city_temp = requests.get(url, params=params)

    try:
        descr = city_temp.json()['weather'][0]['main']
        temp = city_temp.json()['main']['temp']
        return int(temp), descr
    except KeyError:
        flash("The city doesn't exist!", "danger")
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    form = CityForm()
    cities = Cities.query.all()
    if form.validate_on_submit():
        if not get_weather(form.city.data):
            return redirect(url_for('index'))
        temp = get_weather(form.city.data)[0]
        descr = get_weather(form.city.data)[1]
        city_in = Cities.query.filter_by(city_name=form.city.data.upper()).first()
        if city_in:
            flash('The city has already been added to the list!', 'danger')
            return redirect(url_for('index'))
        city = Cities(city_name=form.city.data.upper(), temp=temp, descriptions=descr)
        db.session.add(city)
        db.session.commit()
        flash('Your city has been added!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        for item in cities:
            new_temp = get_weather(item.city_name)[0]
            new_descr = get_weather(item.city_name)[1]
            city = Cities.query.filter_by(city_name=item.city_name).first()
            city.temp = new_temp
            city.descriptions = new_descr
            db.session.commit()
        return render_template('index.html', cities=cities, form=form)
    return render_template('index.html', cities=cities, form=form)


@app.route('/delete/<int:city_id>', methods=['POST', 'GET'])
def delete(city_id):
    city = Cities.query.get(city_id)
    db.session.delete(city)
    db.session.commit()
    flash('Your city has been deleted!', 'success')
    return redirect(url_for('index'))