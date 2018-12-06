from flask import Flask, render_template
import requests
import ephem
from datetime import date, datetime
app = Flask(__name__)

@app.route('/')
def wx():

    obs = ephem.Observer()
    obs.lat = '69.06'
    obs.lon = '18.54'
    obs.pressure = 0
    obs.horizon = '-6'

    obs.date = ephem.Date(datetime.utcnow())
    
    prev_rising = obs.previous_rising(ephem.Sun(), use_center=True)
    next_setting = obs.next_setting(ephem.Sun(), use_center=True)

    ## METAR/TAF

    r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=metar')
    metar = r.text.strip().splitlines()[-1]

    r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=taf')
    taf = r.text.strip().splitlines()[-1]

    return render_template('wx.html', prev_rising=prev_rising, next_setting=next_setting, metar=metar, metar_time="meh", taf=taf)

