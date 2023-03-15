git status
git init
git add .
git commit -m  "textcommit"
git remote add origin https://github.com/nurzadakun/flask_app.git
git push origin master
git checkout -b alinabranch
git branch


set FLASK_APP=newproj
set FLASK_ENV=development
flask run