from flask import Flask, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route("/get")
def get_current_config():
    with open('a.json',"r") as f:
        return "".join(f.readlines())

@app.route("/set", methods=["POST"])
def set_current_config():
    print(request.json)
    with open('a.json',"w") as f:
        json.dump(request.json,f)
    return "nice"
        

if __name__ == '__main__':
    app.run(host="0.0.0.0")