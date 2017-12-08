from flask import Flask, jsonify, abort, make_response
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/inference/<string:path>', methods=['GET'])
def inference(path):
  #推論処理
  # 仮結果
  result = {
        "result":True,
        "data":{
            "hana1":"桜",
            "hana2":"梅",
            "hana3":"ひまわり"
            }
        }
  return make_response(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
  app.run()
