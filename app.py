from flask import Flask, jsonify,request
from flask_cors import CORS
# from NN import temp1
from enum import Enum
from NN import *
import pickle
import os
import requests
import json
import base64



    
    
# configuration
DEBUG = True



# instantiate the appg
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

def toDict(s):
    vis=False
    key=''
    value=''
    cnt=0
    for i in range(len(s)):
        print(vis)
        if s[i]=='{' or s[i]=='"' or s[i]=='}': continue
        elif s[i] ==':' and cnt==0: 
            vis=True 
            cnt=1
            continue
        # :前
        else:
            if vis==False:
                key+=s[i]
            else:
                value+=s[i]
    return {key:value}
                
            
 

                   

# sanity check route
@app.route('/result', methods=['GET','OPTIONS','POST'])
def test():
    if request.method=="POST":
        recv_data = request.get_json()
 
        if recv_data is None:
            # print("request.get_json() is None")
            recv_data = request.get_data()
 
        # print("recv_data=", recv_data)
        json_re = json.loads(bytes.decode(recv_data))
        # print("json_re=", json_re)
        imgRes = json_re['uploadImg']
        # print("imgRes=",imgRes)
 
        imgdata = base64.b64decode(imgRes)
        # print("imgdata=",imgdata)
 
        file = open('./data/test.jpg', "wb")
        file.write(imgdata)
        file.close()
        return jsonify(Test.JudgeGesture(   ))
    return jsonify("next")


if __name__ == '__main__':
    app.run()