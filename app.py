import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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
    #if candname =='Joyce Tick':
    #        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate"), ("pred", prediction)))]))
    #elif candname =='Jack Dup':
    #    op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Appointment booked long ago"), ("pred", prediction)))]))
    #elif candname =='Sam Buca':
    #    op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Varying Job and Native Locations"), ("pred", prediction)))]))
    #else:
    #    op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight",""), ("pred", prediction)))]))
     
    #if prediction < 50 :
    #    if confirmed == "0" and deltday < 7 and JobVsNative == "1":
    #        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate"), ("pred", prediction)))]))
    #    elif confirmed == "1" and deltday >= 7 and JobVsNative == "1":
    #        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Appointment booked long ago"), ("pred", prediction)))]))
    #    elif confirmed == "1" and deltday < 7 and JobVsNative == "0":
    #        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Varying Job and Native Locations"), ("pred", prediction)))]))
    #    else:
    #        op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight",""), ("pred", prediction)))]))
    cond1 = (confirmed == "0")
    cond2 = (deltday < 15)
    cond3 = (JobVsNative == 1)
    
    if prediction < 50:
       if all( [(cond1 == True) , (cond2 == True) , (cond3 == True)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate"), ("pred", prediction)))]))
       elif all( [(cond1 == False) , (cond2 == True) , (cond3 == True)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", ""), ("pred", prediction)))]))
       elif all( [(cond1 == True) , (cond2 == False) , (cond3 == True)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate and Appointment booked long ago"), ("pred", prediction)))]))
       elif all( [(cond1 == False) , (cond2 == False) , (cond3 == True)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Appointment booked long ago"), ("pred", prediction)))]))
       elif all( [(cond1 == True) , (cond2 == True) , (cond3 == False)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate and Varying Job and Native Locations"), ("pred", prediction)))]))              
       elif all( [(cond1 == False) , (cond2 == True) , (cond3 == False)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Varying Job and Native Locations"), ("pred", prediction)))]))
       elif all( [(cond1 == True) , (cond2 == False) , (cond3 == False)] ):
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Confirmation not received from Candidate and Appointment booked long ago and Varying Job and Native Locations"), ("pred", prediction)))]))
       else :
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", "Appointment booked long ago and Varying Job and Native Locations"), ("pred", prediction)))]))
    else :
           op = np.append(op, np.array([dict((("cd", candname),("gender", gender), ("phone", phone), ("Confirmed", confirmed),("scheduler", scheduler), ("jobloc", jobloc), ("natloc", natloc), ("skill",skill), ("JobVsNative", JobVsNative), ("intdt", str(intdt)), ("scdt", str(schdt)), ("insight", ""), ("pred", prediction)))]))
        
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
    #print(dataorg)
    origdict = (dict(enumerate(dataorg)))
    #print(origdict)
    s1 = []
    for d in origdict.values():
        s1.append(d['cd'])
    
    for i in range(0, len(s1)):
        for key in range(i,i+1):
            origdict[s1[i]] = origdict.pop(key)
    
    origdict.update(srcdict)
    #print(origdict)
  
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
 
@app.route('/caldata')
def event_calender():
    base_dir = os.getcwd()
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
            "name": "Schedules", 
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

def genmodel():
    base_dir = os.getcwd()
    data_dir = os.path.join(base_dir, 'Code/RawData')
    #Source File Path
    #in_data_pref = os.path.join(data_dir, 'Input')
    src_file_name = 'InterviewDat.csv'
    src_data_path = os.path.join(data_dir , src_file_name)
    print(src_data_path)

    #Read raw source file for inteview
    df_raw = pd.read_csv(src_data_path, index_col=None, parse_dates=["SchedulingDay", "InterviewDay"], infer_datetime_format=True)
    df_raw["days_delta"] = (df_raw.InterviewDay - pd.to_datetime(df_raw.SchedulingDay.dt.date)).dt.days
    
    # Renaming variables to strings that are a little easier to work with.
    df_raw.columns = ['Candidate_Id', 'Interview_ID', 'Gender', 'Scheduled_Day', 'Interview_Day',
                        'Cand_Loc', 'Job_Loc', 'Venue','Native_Loc','JobVsNative',
                         'Permission(Y/N)', 'MeetingConflict(Y/N)', 'PriorCall(Y/N)', 'AlterantePhone(Y/N)',
                        'ResumePrintout(Y/N)', 'VenueClarification(Y/N)', 'SharedLetter(Y/N)', 'Confirmed', 'Attended',
                         'days_delta']
    df_raw['Cand_Loc'].replace(['- cochin-'],['cochin'], inplace = True)
    df_raw['Job_Loc'].replace(['- cochin-'],['cochin'], inplace = True)
    df_raw['Venue'].replace(['- cochin-'],['cochin'], inplace = True)
    df_raw['Permission(Y/N)'].replace(['na', 'not yet', 'yet to confirm'],['nan', 'tbd', 'tbd'], inplace = True)
    df_raw['MeetingConflict(Y/N)'].replace(['na', 'not sure', 'cant say'],['nan', 'unsure', 'unsure'], inplace = True)
    df_raw['PriorCall(Y/N)'].replace(['na', 'no dont'],['nan', 'no'], inplace = True)
    df_raw['MeetingConflict(Y/N)'].replace(['na', 'not sure', 'cant say'], ['nan', 'unsure', 'unsure'], inplace = True)
    df_raw['AlterantePhone(Y/N)'].replace(['na', 'no i have only thi number'], ['nan', 'no'], inplace = True)
    df_raw['ResumePrintout(Y/N)'].replace(['na', 'not yet', 'no- will take it soon'], ['nan', 'ny', 'ny'], inplace = True)
    df_raw['VenueClarification(Y/N)'].replace(['na', 'no- i need to check'], ['nan', 'no'], inplace = True)
    df_raw['SharedLetter(Y/N)'].replace(['na', 'not sure', 'need to check', 'not yet', 'yet to check','havent checked'],['nan', 'unsure', 'unsure', 'unsure', 'unsure', 'unsure'], inplace = True)
    df_raw['Confirmed'].replace(['Yes', 'No'],[1, 0], inplace = True)
    df_raw['Attended'].replace(['Yes', 'No'],[1, 0], inplace = True)
    
    df_raw['Permission(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['MeetingConflict(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['PriorCall(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['AlterantePhone(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['ResumePrintout(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['VenueClarification(Y/N)'].replace({'Yes':1, 'No':0}, inplace=True)
    df_raw['SharedLetter(Y/N)'].replace({'Yes':1, 'No':0, 'unsure':np.nan}, inplace=True)
    df_raw['JobVsNative'].replace({True:1, False:0}, inplace=True)
    
    df_raw['Permission(Y/N)'].replace({'Yes':1, 'No':0,'Yet to confirm':np.nan, 'NO':0, 'yes':1, 'Na':np.nan,'Not yet':np.nan}, inplace=True)
    df_raw['MeetingConflict(Y/N)'].replace({'Yes':1, 'No':0,'Not Sure':np.nan, 'Not sure':np.nan, 'yes':1, 'Na':np.nan,'cant Say':np.nan}, inplace=True)
    df_raw['PriorCall(Y/N)'].replace({'Yes':1, 'No':0,'yes':1, 'Na':np.nan,'No Dont':np.nan}, inplace=True)
    df_raw['AlterantePhone(Y/N)'].replace({'Yes':1, 'No':0,'yes':1, 'Na':np.nan,'No I have only thi number':0,'nan':np.nan}, inplace=True)
    df_raw['ResumePrintout(Y/N)'].replace({'Yes':1, 'No':0,'yes':1, 'Na':np.nan,'No- will take it soon':0,'nan':np.nan,'Not Yet':0,'Not yet':0}, inplace=True)
    df_raw['VenueClarification(Y/N)'].replace({'Yes':1, 'No':0,'yes':1, 'Na':np.nan,'No- I need to check':0,'nan':np.nan,'Not Yet':0,'Not yet':0,'Na':0,'no':0}, inplace=True)
    df_raw['SharedLetter(Y/N)'].replace({'Yes':1, 'No':0,'yes':1, 'Na':np.nan,'Havent Checked':np.nan,'Need To Check':np.nan, 'Not sure':np.nan,'Yet to Check':np.nan,'Not Sure':np.nan,'nan':np.nan,'Not yet':np.nan,'Not Yet':0,'Not yet':0,'Na':0,'no':0}, inplace=True)
    
    categorical_features = ['Cand_Loc','Job_Loc','Venue','Native_Loc','Gender']
    boolean_features = ['JobVsNative','Permission(Y/N)','MeetingConflict(Y/N)','PriorCall(Y/N)','AlterantePhone(Y/N)','ResumePrintout(Y/N)','VenueClarification(Y/N)','SharedLetter(Y/N)','Confirmed']

    for feature in boolean_features:
        df_raw[feature] = df_raw[feature].astype("bool")

    for feature in categorical_features:
        df_raw[feature] = df_raw[feature].astype("category")
        
    df_raw['Permission(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['MeetingConflict(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['PriorCall(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['AlterantePhone(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['ResumePrintout(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['VenueClarification(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['SharedLetter(Y/N)'].replace({True:1, False:0}, inplace=True)
    df_raw['JobVsNative'].replace({True:1, False:0}, inplace=True)
    df_raw['Confirmed'].replace({True:1, False:0}, inplace=True)
    
    one_hot_features = pd.get_dummies(df_raw.drop(["Candidate_Id","Interview_ID","Scheduled_Day","Interview_Day","Native_Loc","Venue","Job_Loc","Cand_Loc","Native_Loc","Gender","Attended"], axis=1)).columns
    print(one_hot_features)
    
    X = pd.get_dummies(df_raw.drop(["Candidate_Id","Interview_ID","Scheduled_Day","Interview_Day","Native_Loc","Venue","Job_Loc","Cand_Loc","Native_Loc","Gender","Attended"], axis=1)).values
    y = df_raw['Attended'].values

    X = X.astype("float64")
    y = y.astype("float64")

    X = df_raw[one_hot_features]
    y = df_raw["Attended"]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.4, shuffle = True)
    X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=.5, shuffle = True)
    
    train_df = pd.DataFrame(data=X_train, columns=one_hot_features)
    train_df["Attended"] = y_train
    
    rf = RandomForestClassifier(max_depth=5, n_estimators=10)
    model_rf = rf.fit(X_train,y_train)
    y_pred_rf = model_rf.predict(X_test)
    
    #Saving the model to disk
    pickle.dump(model_rf, open('model.pkl', 'wb'))

genmodel()   


#@app.route('/refresh', methods=['GET', 'POST'])
#def refresh():
#    pyautogui.hotkey('ctrl', 'f5')
#    return render_template('appointment.html')

if __name__ == "__main__":
    app.run(debug=True)
    
    
