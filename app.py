import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from datetime import datetime
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('home.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

op = np.array([dict((("cd", ""), ("gender", ""), ("phone", ""), ("Confirmed",0), ("scheduler",""), ("jobloc", ""), ("natloc", ""), ("skill", ""), ("JobVsNative", 0), ("intdt", str(datetime.strptime('1900-01-01', '%Y-%m-%d').date())), ("scdt", str(datetime.strptime('1900-01-01', '%Y-%m-%d').date())), ("insight",""), ("pred", 0)))])
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    import json
    import os

    src_path = os.getcwd()
    int1_data_path = src_path + '/Data/Output/int1.json'
    int2_data_path = src_path + '/Data/Output/int2.json'
    int3_data_path = src_path + '/Data/Output/int3.json'
    finop_data_path = src_path + '/static/json/JSON_Data.json'
    finop1_data_path = src_path + '/Data/Output/finalop1.json'
    candname = str(request.values.get("Name"))
    #age = request.values.get("Age")
    gender = request.values.get("Gender")
    phone = request.values.get("Phone")
    #lstremdt = request.values.get("Last Reminder")
    #sms = request.values.get("Sms Received")
    skill = request.values.get("Skill")
    scheduler = request.values.get("Scheduler")
    jobloc = request.values.get("Job Location")
    natloc = request.values.get("Native Location")
    confirmed = request.values.get("Confirmation")
    
    
    if request.values.get("Interview Date") == None:
        intdt = datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    else:
        intdt = datetime.strptime(request.values.get("Interview Date"), '%Y-%m-%d').date()
    
    if request.values.get("Schedule Date") == None:
        schdt = datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    else:
        schdt = datetime.strptime(request.values.get("Schedule Date"), '%Y-%m-%d').date()
    
    deltday = abs((intdt - schdt).days)
    #if request.values.get("Sms Received") == 1:
    #    smspred = 0
    #else:
    #    smspred = 1
    
    if request.values.get("Job Location") == request.values.get("Native Location"):
        JobVsNative = 1
    else:
        JobVsNative = 0
    
    inp = np.array([JobVsNative, 1, 1, 1, 1, 1, 1, 1, confirmed, deltday]).reshape(1, 10)
    
    if request.values.get("Skill") == None:
        prediction = 0
    else:
        prediction = round(model.predict_proba(inp)[0][1] *100, 2)      
   
    global op
    if candname =='Joyce Tick':
        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate"), ("pred", prediction)))]))
    elif candname =='Jack Dup':
        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Appointment booked long ago"), ("pred", prediction)))]))
    elif candname =='Sam Buca':
        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Varying Job and Native Locations"), ("pred", prediction)))]))
    else:
        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight",""), ("pred", prediction)))]))
     
    oplist = op.tolist()
    oplist.pop(0)
    print(oplist)
    srcdict = (dict(enumerate(oplist)))
    
    s = []
    for d in srcdict.values():
        s.append(d['cd'])
    
    for i in range(0, len(s)):
        for key in range(i,i+1):
            srcdict[s[i]] = srcdict.pop(key)
      
    with open(finop_data_path, "r") as f:
        lines = (str(f.readlines())[10::])
        lines = (lines[:len(lines)-4])
    #print(lines)
    
    with open(int1_data_path, "w") as f:
        f.write(lines)
        f.close()
    
    with open(int1_data_path, "r") as f:
        dataorg = json.load(f)
        f.close()
    print(dataorg)
    origdict = (dict(enumerate(dataorg)))
    print(origdict)
    s1 = []
    for d in origdict.values():
        s1.append(d['cd'])
    
    for i in range(0, len(s1)):
        for key in range(i,i+1):
            origdict[s1[i]] = origdict.pop(key)
    
    origdict.update(srcdict)
    print(origdict)
  
    with open(int2_data_path, "w") as f:
        json.dump(origdict, f)
        f.close() 
   
    l = []
    for i in origdict.keys():
        l.append(origdict[i])
        
    with open(int3_data_path, "w") as f:
        json.dump(l, f)
        f.close()
    
    with open(int3_data_path, "w") as f:
        f.write(str(l).replace("'", "\""))
        f.close()
        
    with open(int3_data_path, "r") as f:
        lines = (str(f.readlines())[1::])
        lines = (lines[:len(lines)-1])
        finop = 'data =' + lines
    
    with open(finop_data_path, "w") as f:
        f.write(finop)
        f.close()
        
    return render_template('appointment.html', prediction_text = 'Attendance Chance {} %'.format(prediction), candidate_name = format(candname))
    
#@app.route('/refresh', methods=['GET', 'POST'])
#def refresh():
#    pyautogui.hotkey('ctrl', 'f5')
#    return render_template('appointment.html')

if __name__ == "__main__":
    app.run(debug=True)
    
    
