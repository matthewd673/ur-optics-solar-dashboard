from os import access
import time
from flask import Flask, request, jsonify, send_file, redirect, session, Response, flash
import datetime
import flask
from flask.helpers import get_flashed_messages
import pytz
import csv
from decouple import config
import requests
from boxsdk import Client, OAuth2
import secrets
import json

from flask_pymongo import PyMongo

# my_date = datetime.datetime.now(pytz.timezone('US/New_York'))



global counter
counter = 0

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/solar_dashboard_database")
db = mongodb_client.db

#box api info
box_client_id = config('BOX_CLIENT_ID')
box_client_secret = config('BOX_CLIENT_SECRET')

#box api
def store_tokens(access_token, refresh_token): #TODO: DON'T DO THIS
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token

box_oauth = OAuth2(
    client_id=box_client_id,
    client_secret=box_client_secret,
    store_tokens=store_tokens
)

box_client = Client(box_oauth)

box_auth_url, box_csrf_token = box_oauth.get_authorization_url('http://localhost:5000/box/auth_redirect')

# db.test.insert_one({'title': "todo title", 'body': "todo body"})
@app.route('/test_insert')
def test_insert():
    db.test.insert_one({'title': "todo title", 'body': "todo body"})
    return jsonify(message="success")

@app.route("/test_find")
def home():
    test = db.test.find()
    for t in test:
        print(t)
    return jsonify([t for t in test])


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/livedata')
def get_sample_data():
    global counter
    counter += 1
    return {
        'time': datetime.datetime.now(pytz.timezone('America/New_York')),
        'irradiance' : {
            'global_horizontal': 0+counter,
            'direct_normal' : 0+counter,
            'diffuse_horizontal' : 0+counter,
        },
        'meteorological' : {
            'pr1_temperature' : 0+counter,
            'ph1_temperature': 0+counter,
            'pressure' : 0+counter,
            'zenith_angle' : 0+counter,
            'azimuth_angle' : 0+counter,
            'razon_status' : 0+counter,
            'razon_time' : 0+counter,
            'logger_battery' : 0+counter,
            'logger_temp' : 0+counter,
        },
        'units' : {
            'global_horizontal': "u",
            'direct_normal' : "u",
            'diffuse_horizontal' : "u",
            'pr1_temperature' : "u",
            'ph1_temperature': "u",
            'pressure' : "u",
            'zenith_angle' : "u",
            'azimuth_angle' : "u",
            'razon_status' : "u",
            'razon_time' : "u",
            'logger_battery' : "u",
            'logger_temp' : "u",
        }
    }

@app.route('/graph')
def get_sample_graph_data():
    # request.args.get('page', 1)
    arguments = {
        "irradiance-global-horizontal": 4,
        "irradiance-direct-normal": 5,
        "irradiance-diffuse-horizontal": 6,
        "meteorological-pr1-temperature": 7,
        "meteorological-ph1-temperature": 8,
        "meteorological-pressure": 9,
        "meteorological-zenith-angle": 10,
        "meteorological-azimuth-angle": 11,
        "meteorological-razon-status": 12,
        "meteorological-razon-time": 13,
        "meteorological-logger-battery": 14,
        "meteorological-logger-temp": 15    
    }

    includedData = [
        # 1,2,3,
        # 4,5,
        # 9,13
        ]

    for key, value in arguments.items():
        if(request.args.get(key) != None and request.args.get(key).lower()=="true"):
            includedData.append(value)

    print(includedData)

    headerDataDict = {
        "":0,
        "Year":1,
        "DOY":2,
        "MST":3,
        "Global Horizontal [W/m^2]":4,
        "Direct Normal [W/m^2]":5,
        "Diffuse Horizontal [W/m^2]":6,
        "PR1 Temperature [deg C]":7,
        "PH1 Temperature [deg C]":8,
        "Pressure [mBar]":9,
	    "Zenith Angle [degrees]":10,
        "Azimuth Angle [degrees]":11,
        "RaZON Status":12,
        "RaZON Time [hhmm]":13,
        "Logger Battery [VDC]":14,
        "Logger Temp [deg C]":15,
    }

    headerDataList = [
        "", # 0
        "Year",     # 1
        "DOY",      # 2
        "MST",      # 3
        "Global Horizontal [W/m^2]",    # 4
        "Direct Normal [W/m^2]",        # 5
        "Diffuse Horizontal [W/m^2]",
        "PR1 Temperature [deg C]", 
        "PH1 Temperature [deg C]",
        "Pressure [mBar]",              # 9
	    "Zenith Angle [degrees]",
        "Azimuth Angle [degrees]",
        "RaZON Status",
        "RaZON Time [hhmm]",            # 13
        "Logger Battery [VDC]",
        "Logger Temp [deg C]",
    ]

    irridianceDataList = ["Global Horizontal [W/m^2]",    # 4
        "Direct Normal [W/m^2]",        # 5
        "Diffuse Horizontal [W/m^2]",]

    meteorologicalDataList = ["PR1 Temperature [deg C]", 
        "PH1 Temperature [deg C]",
        "Pressure [mBar]",              # 9
	    "Zenith Angle [degrees]",
        "Azimuth Angle [degrees]",
        "RaZON Status",
        "RaZON Time [hhmm]",            # 13
        "Logger Battery [VDC]",
        "Logger Temp [deg C]",]

    graphList = []

    # print('hello')
    with open('20210629.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        header = next(csv_reader)
        # print(header)
        # for h in header:
        #     graph[h] = []
        count = 1
        for lines in csv_reader:
            count+=1
            # if(count>10):
            #     break
        
            point = {}

            hour = lines[3][:-2]
            if(hour==""):
                hour = "0"
            dt = datetime.datetime.strptime(f"{lines[1]} {lines[2]} {hour}:{lines[3][-2:]}", '%Y %j %H:%M')
            dt= dt.replace(tzinfo=pytz.timezone('America/New_York'))

            point["date"] = dt.strftime('%x')
            # if(hour == "0" and lines[3][-2:]=="0"):
            #     point["date"] = dt.strftime('%x')
            
                # print("000000")
            # print(f"DT: {dt.strftime('%x')}")
            # print("Created at {:d}:{:02d}".format(int(hour), int(lines[3][-2:])))
            # print(dt.time())
            # dt.strftime("%-I:%M %p")

            point["datetime"] = dt.strftime("%I:%M %p").lstrip("0")
            # "{:d}:{:02d}".format(int(hour), int(lines[3][-2:]))

            # print(f"year: {lines[1]}\tdoy:{lines[2]}\tmst:{lines[3]}\t{lines[3][:-2]}...{lines[3][-2:]}")
            for include in includedData:
                point[headerDataList[include]] = float(lines[include])
            # print(point)
            graphList.append(point)
            # print(lines[4], lines[5], lines[13])

        includedHeaderStrings = {}

        irridianceHeaderStrings = []
        meteorologicalHeaderString = []
        for i,include in enumerate(includedData):
            includedHeaderStrings[headerDataList[include]] = i

            if(headerDataList[include] in irridianceDataList):
                irridianceHeaderStrings.append(headerDataList[include])

            elif(headerDataList[include] in meteorologicalDataList):
                meteorologicalHeaderString.append(headerDataList[include])

        print(includedHeaderStrings)
        print(irridianceHeaderStrings)
        print(meteorologicalHeaderString)

    return {"return_data":graphList, "included_headers":includedHeaderStrings, "irridiance_headers":irridianceHeaderStrings,"meteorological_headers":meteorologicalHeaderString}

@app.route('/get_csv')
def get_csv():

    # Send the file back to the client
    return send_file("./CR300Series_DataOut.csv", as_attachment=True, attachment_filename="CR300Series_DataOut.csv")


def make_box_request(path):
    bearer_token = 'none' #this way we'll at least get a 403 before everything breaks
    if session.get('access_token') == None:
        flash('No access token', 'error')
    else:
        bearer_token = session['access_token']
    
    headers = { 'Authorization': 'Bearer ' + bearer_token,
                'Content-Type': 'application/json' }
    r = requests.get('https://api.box.com/2.0' + path, headers=headers)
    r.close()

    if r.status_code != 200:
        flash('Box API returned ' + str(r.status_code))
        return None #make it easier for the other methods to check for errors
    
    return r

@app.route('/box/get_has_auth')
def get_box_has_auth():
    if session.get('access_token') is not None:
        return 'true'
    return 'false'

@app.route('/box/get_auth_url')
def get_box_auth_url():
    return redirect(box_auth_url, code=302) #302 because auth link can change. I think that makes sense.

@app.route('/box/auth_redirect', methods=['GET'])
def box_auth_redirect():
    state = request.args.get('state') #should match box_csrf_token
    code = request.args.get('code')

    if state != box_csrf_token: #error if csrf tokens dont match
        flash('Something went wrong when authenticating (CSRF tokens do not match).', 'error')
        return redirect('http://localhost:3000/', code=302)
        #return 'Tokens do not match'
    access_token, refresh_token = box_oauth.authenticate(code)

    return redirect('http://localhost:3000/', code=302)

@app.route('/box/get_csv/<file_id>', methods=['GET'])
def box_get_csv(file_id):
    r = make_box_request('/files/' + file_id + '/content')
    
    if r == None: #TODO: temporary, but better
        flash('Could not download from Box', 'error')
        return ''
    
    file = r.content
    return Response(file, mimetype='text/csv')

@app.route('/box/get_folder_csvs/<folder_id>', methods=['GET'])
def box_get_folder_csvs(folder_id):
    r = make_box_request('/folders/' + folder_id + '/items/')
    
    if r == None: #TODO: temporary, but better
        flash('Could not read Box folder', 'error')
        return ''
    
    folder = r.json();
    ct = folder['total_count']
    entries = folder['entries']

    file_ids = []
    for entry in entries:
        if (entry['name'].endswith('.csv')):
            file_ids.append(entry['id'])
    output = {}
    output['files'] = file_ids
    output_json = json.dumps(output)
    return Response(output_json, mimetype='application/json')

@app.route('/box/get_user_info')
def box_get_user_info():
    r = make_box_request('/users/me')

    if r == None: #TODO: temporary, but better
        flash('Could not get user info', 'error')
        return ''

    return r.json()

@app.route('/get_flashes')
def get_flashes():
    output = {}
    flashlist = []
    for f in get_flashed_messages(with_categories=True):
        flashlist.append({ 'text': f[1], 'category': f[0] })
    output['flashes'] = flashlist
    output_json = json.dumps(output)

    session.pop('_flashes', None) #TODO: flash messages won't clear
    flashlist = []
    return Response(output_json, mimetype='application/json')