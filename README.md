# inference

##  .skipPythonDeployment
Azure API APPS にデプロイする時に仮想環境とライブラリをインストール不要にする。
その代わりD:\home\python361x64\にPythonとライブラリをインストールしてあげる必要がある。

##  main.py
アプリのメイン。

##  ptvs_virtualenv_proxy.py
不要。
サンプルでは仮想環境で動作させるため、起動時にこれを実行し仮想環境を有効にする的なことをしている。

##  requirements.txt
必要なライブラリを記載する。
.skipPythonDeploymentない場合、デプロイするときにAzure側がこのファイルを参照しライブラリをインストールしてくれます。

##  web.config
設定

# インストール
1. API APS作成
2. 拡張機能からPython3.6.1x64インストール
3. ハンドラーマッピング設定
fastCgi D:\home\python361x64\python.exe D:\home\python361x64\wfastcgi.py
4. デプロイオプション設定
5. Kuduからライブラリインストール
