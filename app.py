import git
import os
from flask import Flask, request, jsonify, render_template
from git import Repo

app = Flask(__name__)

@app.route('/')
def event_calender():
    src_path = os.getcwd()
    print(src_path)
    finop_data_path = src_path + '/static/json/JSON_Data.json'
    print(finop_data_path)
    destbranch = git checkout caldata
    print(destbranch)

if __name__ == "__main__":
    app.run(debug=True)
    
    
