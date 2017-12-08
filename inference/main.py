# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response
import json

api = Flask(__name__)

@api.route('/inference/<string:path>', methods=['GET'])
def inference(path):
    # 推論処理

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

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
  api.run()                                                                                                                                                                                                                                                                                                                                                                                                                     