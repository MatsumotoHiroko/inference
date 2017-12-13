from flask import Flask, jsonify, abort, make_response
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import json
import sys
import cntk
import logs # Debug

app = Flask(__name__)
app.config['DEBUG'] = True # Debug
logs.init_app(app)

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
            },
         "cntk version": cntk.__version__
        }
  return make_response(json.dumps(result, ensure_ascii=False))

#@app.route('/inference', methods=['POST'])
#def inference_binary():
#  return 'coming soon'

@app.route('/test', methods=['GET'])
def test():
    return "test"

@app.route('/blob', methods=['GET'])
def blob():
    block_blob_service = BlockBlobService(account_name='hanastragetest', account_key='acount_key')
    app.logger.info("test message : {}".format(block_blob_service))
    # container create
    block_blob_service.create_container('images')
    block_blob_service.set_container_acl('images', public_access=PublicAccess.Container)
    #app.logger.info("finish : block_blob_service.set_container_acl")

    # delete
    block_blob_service.delete_blob('images', 'sunflower.png')
    
    # blob write
    block_blob_service.create_blob_from_path(
        'images',
        'sunflower.png',
        'D:\home\site\wwwroot\static\sunflower.png',
        content_settings=ContentSettings(content_type='image/png')
                )

    # get container
    generator = block_blob_service.list_blobs('images')
    for blob in generator:
        app.logger.info("generator : {}".format(blob.name))
    #app.logger.info("generator_object : {}".format(generator))


    result = {
            "result":True,
            "data":{
                "blob_name": [blob.name for blob in generator]
                }
            }
    return make_response(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
  app.run()
