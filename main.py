from flask import Flask, jsonify, abort, make_response
import json
import sys
#import cntk
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!' + sys.version

@app.route('/inference', methods=['GET'])
def inference():
  result = {
        "result":True,
        "data":{
            "hana1":"桜",
            "hana2":"梅",
            "hana3":"ひまわり"
            }
        }
  return make_response(json.dumps(result, ensure_ascii=False))

#@app.route('/inference', methods=['POST'])
#def inference_binary():
#  return 'coming soon'

if __name__ == '__main__':
  app.run()
