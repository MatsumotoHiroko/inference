from flask import Flask, jsonify, abort, make_response
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@api.route('/inference/<string:path>', methods=['GET'])
def inference(path):
  # ���_����
  # ������
  result = {
        "result":True,
        "data":{
            "hana1":"��",
            "hana2":"�~",
            "hana3":"�Ђ܂��"
            }
        }
  return make_response(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
  app.run()
