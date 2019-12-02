# personality_analysis
クイズアプリ用API

## 起動方法
pycharmではなくコマンドでの実行方法。<br>
下記コマンドでdocker起動

`docker-compose up -d`

コンテナに入り、サーバー起動

`docker exec -it {コンテナ名} sh`

`python manage.py runserver 0.0.0.0:8000`

## API詳細
doc/swagger.ymlを参照
