from flask import Flask, jsonify, abort, make_response
# blob module
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
# file module
from azure.storage.file import FileService
from azure.storage.file import ContentSettings

import json
import sys
import cntk
import logs # Debug
import os
import os.path

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
    static_dir_path = "D:\home\site\wwwroot\static"
    account_name = 'hanastragetest'
    account_key = 'acount_key'
    container_name = 'images'
    container_url = "https://hanastragetest.blob.core.windows.net/" + container_name

    block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    app.logger.info("test message : {}".format(block_blob_service))
    # container create
    block_blob_service.create_container(container_name)
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
    #app.logger.info("finish : block_blob_service.set_container_acl")

    files = os.listdir(static_dir_path)
    for file in files:
        # delete
        if block_blob_service.exists(container_name, file):
            block_blob_service.delete_blob(container_name, file)

        # blob write
        block_blob_service.create_blob_from_path(
            container_name,
            file,
            static_dir_path + '\\' + file,
            content_settings=ContentSettings(content_type='image/png')
                    )

    # get container
    generator = block_blob_service.list_blobs(container_name)
    html = ""
    for blob in generator:
        #app.logger.info("generator : {}".format(blob.name))
        html = "{}<img src='{}/{}'>".format(html, container_url, blob.name)
    #app.logger.info("generator_object : {}".format(generator))

    result = {
            "result":True,
            "data":{
                "blob_name": [blob.name for blob in generator]
                }
            }
    return make_response(json.dumps(result, ensure_ascii=False) + html)

@app.route('/file', methods=['GET'])
def file():
    static_dir_path = "D:\home\site\wwwroot\static"
    static_file_dir_path = static_dir_path + '\\' + 'files'
    account_name = 'hanastragetest'
    account_key = 'acount_key'
    root_share_name = 'root'
    share_name = 'images'
    directory_url = 'https://hanastragetest.file.core.windows.net/' + root_share_name + '/' + share_name

    # create local save directory
    if os.path.exist(static_file_dir_path) is False:
        os.mkdir(static_file_dir_path)

    file_service = FileService(account_name=account_name, account_key=account_key)
    # create share
    file_service.create_share(root_share_name)

    # create directory
    file_service.create_directory(root_share_name, share_name)

    files = os.listdir(static_dir_path)
    for file in files:
         # delete
        if file_service.exists(root_share_name, share_name, file):
            file_service.delete_file(root_share_name, share_name, file)
       
        # file upload
        file_service.create_file_from_path(
        root_share_name,
        share_name, # We want to create this blob in the root directory, so we specify None for the directory_name
        file,
        static_dir_path + '\\' + file,
        content_settings=ContentSettings(content_type='image/png'))

    generator = file_service.list_directories_and_files(root_share_name, share_name)

    html = ""
    for file in generator:
        # file download
        file_save_path = static_file_dir_path + '\\' + file
        file_service.get_file_to_path(root_share_name, share_name, file, file_save_path)
        html = "{}<img src='{}'>".format(html, file_save_path)

    result = {
            "result":True,
            "data":{
                "file_or_dir_name": [file_or_dir.name for file_or_dir in generator]
                }
            }
    return make_response(json.dumps(result, ensure_ascii=False) + html)


if __name__ == '__main__':
  app.run()
