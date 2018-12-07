from flask import Flask, render_template
import requests
import ephem
from datetime import date, datetime
app = Flask(__name__)

@app.route('/')
def wx():

    # Setup ENDU Bardufoss
    obs = ephem.Observer()
    obs.lat = '69.06'
    obs.lon = '18.54'
    obs.pressure = 0
    obs.horizon = '-6'

    obs.date = ephem.Date(datetime.fromordinal(date.today().toordinal()))
    
    next_rising = obs.next_rising(ephem.Sun(), use_center=True)
    next_setting = obs.next_setting(ephem.Sun(), use_center=True)

    ## METAR/TAF

    r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=metar')
    metar = r.text.strip().splitlines()[-1]

    r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=taf')
    taf = r.text.strip().splitlines()[-1]

    rising_utc = next_rising.datetime().strftime("%H:%M")
    rising_lt  = ephem.localtime(next_rising).strftime("%H:%M")
    setting_utc = next_setting.datetime().strftime("%H:%M")
    setting_lt = ephem.localtime(next_setting).strftime("%H:%M")

    rising_time = "%sUTC (%sLT)" % (rising_utc, rising_lt)
    setting_time = "%sUTC (%sLT)" % (setting_utc, setting_lt)

    return render_template('wx.html', rising=rising_time, setting=setting_time, metar=metar, metar_time="meh", taf=taf)

