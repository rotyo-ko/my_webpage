# 簡易掲示板アプリ

## 概要

このプロジェクトは、Django の学習目的で作成した Web アプリケーションです。
モデル設計、CRUD 処理、認証まわりの理解を目的としています。

ログイン、未ログインどちらでも投稿でき、
ログイン時はユーザー名、未ログイン時は"ゲスト"と投稿者名が表示されます。

また、Django REST FrameworkによってWeb APIの CRUD を実装しています。
  
viewsはFBVで実装していますが、学習として同じ動作ができるようなCBVの実装をcbv_views.py, cbv_urls.pyとして残してあります。
  

## データベースについて

  開発はPostgreSQLでおこないましたが、このリポジトリではSQLite3を使用しています。
  
  また、環境変数の管理にdjango-environを導入しているので.envを設定していただければPostgreSQLでも実行できるようになっています。
  .env.exampleを参考に.envを設定してください。そのままでしたらSQLite3で実行できます。
  

## 導入方法

  
```bash  
git clone https://github.com/rotyo-ko/my_webpage
# git がないときは zipファイルをダウンロードしてください。

cd my_webpage

# .env の作成
# .env.example をコピーして .env を作成してください

# 仮想環境の作成
python -m venv venv
  
# 仮想環境の有効化
venv\Scripts\activate  # Windows
source venv/bin/activate # Mac

# パッケージのインストール
pip install -r requirements.txt
```
## SECRET_KEY の設定

Django を起動するには SECRET_KEY が必要です。

以下のコマンドを実行して、表示された文字列を .env のSECRET_KEY に設定してください。


```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 
```
```bash
# マイグレーション と　サーバー起動
python manage.py migrate
python manage.py runserver
```
  
### ブラウザでアクセス
http://127.0.0.1:8000/
  
### Web API にブラウザでアクセス
http://127.0.0.1:8000/api/comments

http://127.0.0.1:8000/api/my-comments

## テストの実行
ブラウザ、WebAPIのテストがあります
```bash
python manage.py test
```
