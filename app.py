import os
from flask import Flask, request, jsonify, render_template
import pygit
import git

app = Flask(__name__)

@app.route('/')
def event_calender():
    src_path = os.getcwd()
    print(src_path)
    finop_data_path = src_path + '/static/json/JSON_Data.json'
    print(finop_data_path)
    git = repo.git
    git.checkout('HEAD', b="my_new_branch")
    previous_branch = repo.active_branch
    print(previous_branch)

if __name__ == "__main__":
    app.run(debug=True)
    
    
