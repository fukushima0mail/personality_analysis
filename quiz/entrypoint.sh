#!/bin/sh

## 暫定的にDBの接続情報を記述(環境変数の設定ができるようになったら消すべき)
DB_SERVER=db
DB_NAME=quiz
DB_USER=root
DB_PASSWORD=password

wait_sql() {
  mysql -h ${DB_SERVER} -u ${DB_USER} -p"${DB_PASSWORD}" -e"$1" --default-character-set=utf8mb4  ${DB_NAME}
}

exec_sql() {
  mysql -h ${DB_SERVER} -u ${DB_USER} -p"${DB_PASSWORD}" --default-character-set=utf8mb4  ${DB_NAME} < "$1"
}

wait_mysql() {
  echo "Waiting for mysql"
  until wait_sql 'status' &> /dev/null
  do
          echo -n "."
          sleep 1
  done
}

# mysqlの起動待ち
wait_mysql

# migrate
python manage.py migrate

# DBデータ初期化
exec_sql './testdata/quiz_user_insdata.sql'
exec_sql './testdata/quiz_group_insdata.sql'
exec_sql './testdata/quiz_question_insdata.sql'
#exec_sql 'insert into quiz_user
#(user_id,user_name,mail_address,authority,is_deleted,create_date,update_date)
#values
#("78cca1a7720b4298b5fed84e0b813173","テストユーザ1","aaa@xxx.jp","0","0","2019/11/23","2019/11/23")
#;'

# サーバ起動
python