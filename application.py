from flask import Flask, render_template
import requests
import ephem
from datetime import date, datetime, time
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

    rising_utc = next_rising.datetime().strftime("%H:%M")
    rising_lt  = ephem.localtime(next_rising).strftime("%H:%M")
    setting_utc = next_setting.datetime().strftime("%H:%M")
    setting_lt = ephem.localtime(next_setting).strftime("%H:%M")

    rising_time = "%sUTC (%sLT)" % (rising_utc, rising_lt)
    setting_time = "%sUTC (%sLT)" % (setting_utc, setting_lt)

    ## METAR/TAF
    
    try:
        metar_r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=metar')
        taf_r = requests.get('https://api.met.no/weatherapi/tafmetar/1.0/?icao=ENDU&content_type=text/plain&content=taf')
    except ConnectionError:
        return '<h1>Cannot connect to met.no.</h1>'

    metar = metar_r.text.strip().splitlines()[-1]
    taf = taf_r.text.strip().splitlines()[-1]

    # Shittiest code ever, but works
    metar_hrs, metar_min = (int(metar[7:9]), int(metar[9:11]))
    taf_hrs, taf_min = (int(taf[7:9]), int(taf[9:11]))

    metar_time = datetime.combine(date.today(), time(metar_hrs, metar_min))
    taf_time = datetime.combine(date.today(), time(taf_hrs, taf_min))

    metar_time_str = metar_time.strftime("%H:%M")
    taf_time_str = taf_time.strftime("%H:%M")

    # TODO: Clean up and factor out this ugly formatting code
    metar_ago = (datetime.utcnow() - metar_time).total_seconds() // 60
    metar_ago_str = "%d %s ago" % (metar_ago, "minute" if metar_ago == 1 else "minutes")

    taf_ago = (datetime.utcnow() - taf_time).total_seconds() // 60
    taf_ago_str = "%d %s ago" % (taf_ago, "minute" if taf_ago == 1 else "minutes")

    return render_template('wx.html', 
            rising=rising_time, setting=setting_time, 
            metar=metar, metar_time=metar_time_str, metar_ago=metar_ago_str,
            taf=taf, taf_time=taf_time_str, taf_ago=taf_ago_str)

