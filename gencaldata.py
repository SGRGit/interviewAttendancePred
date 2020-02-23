import json
from flask import Flask, jsonify
import os
import sys
import pandas as pd
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def event_calender():
    base_dir = os.getcwd()
    print(base_dir, sys.path)
    data_path = base_dir + '/static/json/JSON_Data.json'

    with open(data_path, "r") as f:
        lines = str(f.readlines())
	
	#Format the patient json to json format
    a = lines.split("data =")[1]
    a = a.split("\'")[1]
    a = a.split("]")[0]
    a = a.split("[")[1]

	#Create Dictionary
    dic = eval(a)

	#Create Derived Columns
    for i in range(len(dic)):
        if (dic[i]['Confirmed']) == '1':
            dic[i]['Cnf'] = 1
        else:
            dic[i]['Cnf'] = 0
    
    for i in range(len(dic)):
        if (dic[i]['pred']) > 50:
            dic[i]['High'] = 1
        else:
            dic[i]['High'] = 0
    
    for i in range(len(dic)):
        if (dic[i]['pred']) <= 50:
            dic[i]['Lo'] = 1
        else:
            dic[i]['Lo'] = 0

	#Convert to dataframe
    diclist = list(dic)
    df = pd.DataFrame(diclist)
    df_new = pd.DataFrame()
    df_new = df [['cd']]
    df_new['intdt'] = df [['intdt']]
    df_new['High'] = df [['High']]
    df_new['Lo'] = df [['Lo']]
    df_new['Cnf'] = df [['Cnf']]

	#Calculate aggregate metrices
    df_op = df_new.groupby(['intdt'])['High'].sum()
    df_op = df_op.to_frame()
    df_op['Lo'] = df_new.groupby(['intdt'])['Lo'].sum()
    df_op['Cnf'] = df_new.groupby(['intdt'])['Cnf'].sum()
    df_op['Total'] = df_new.groupby(['intdt'])['cd'].count()
    df_op = df_op.reset_index()
    df_op = df_op.rename(columns={"intdt": "date"})

	#Convert to Dictionary
    df_dict = df_op.to_dict('records')
    
    dlist = []
    for i in range(len(df_dict)):
        df_newdict = {
        "date": df_dict[i]['date'],
        "event": [
            {
            "color": "violet", 
            "name": "Appointments", 
            "value": df_dict[i]['Total']
            }, 
            #{
            #"color": "green", 
            #"name": "Confirmed", 
            #"value": df_dict[i]['Cnf']
            #}, 
            {
            "color": "red", 
            "name": "Low Probability", 
            "value": df_dict[i]['Lo']
            }, 
            {
            "color": "amber", 
            "name": "High Probability", 
            "value": df_dict[i]['High']
            }]
            }
        dlist.append(df_newdict.copy())

    return(jsonify(dlist))
if __name__ == "__main__":
    app.run(debug=True)	

#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port='7000', threaded=True, debug=True)
