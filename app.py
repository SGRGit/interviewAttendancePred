import os
import pygit
from git import Repo

app = Flask(__name__)

@app.route('/')
def event_calender():
    src_path = os.getcwd()
    print(src_path)
    finop_data_path = src_path + '/static/json/JSON_Data.json'
    print(finop_data_path)
    repo = git.Repo()
    previous_branch = repo.active_branch
    print(previous_branch)

if __name__ == "__main__":
    app.run(debug=True)
    
    
