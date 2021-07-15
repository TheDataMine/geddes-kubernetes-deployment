#Required Packages
import json
from flask import Flask, jsonify, request
import sys
import random

#Handle Internal Packages
sys.path.append("/workspace/GitHub/geddes-kubernetes-deployment/src/")
sys.path.append("./src/")

#Internal Package(s)
from utils import fun

#Establish App
app = Flask(__name__)

#Functions
#Default
@app.route('/')
def index():
    return jsonify({'name': 'Justin A. Gould',
                    'email': 'gould29@purdue.edu',
                    'number': '248-877-0751',
                    'message': f'{random.randrange(20, 50, 3)}'})

#Combined Split and Tokenize
@app.route('/add_two', methods=["POST"])
def add_two_function():
    #Run Function
    p = request.get_json()
    
    output = fun.add_two(p["num"])
    print(output)
    return jsonify({'output': output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)