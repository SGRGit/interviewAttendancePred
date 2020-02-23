import os
import pygit

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def event_calender():
    src_path = os.getcwd()
    print(src_path)
    finop_data_path = src_path + '/static/json/JSON_Data.json'
    print(finop_data_path)
    git checkout caldata finop_data_path

if __name__ == "__main__":
    app.run(debug=True)
    
    
