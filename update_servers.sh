#!/bin/bash
BRANCH="origin atomictransactions"
#git add --all
#git commit -m "$1"
#git push $BRANCH
cd ~/Documents/Work/Distributed\ Systems/1000/octokart
find . -name "*.pyc" -exec rm -rf {} \;
#git pull $BRANCH
cd octokart
if [ "$2" = "migrate" ]
then
    python manage.py makemigrations
    python manage.py migrate
fi
cd ../../..
cd ~/Documents/Work/Distributed\ Systems/2000/octokart
find . -name "*.pyc" -exec rm -rf {} \;
#git pull $BRANCH
cd octokart
if [ "$2" = "migrate" ]
then
    python manage.py makemigrations
    python manage.py migrate
fi
cd ../../..
cd ~/Documents/Work/Distributed\ Systems/3000/octokart
find . -name "*.pyc" -exec rm -rf {} \;
#git pull $BRANCH
cd octokart
if [ "$2" = "migrate" ]
then
    python manage.py makemigrations
    python manage.py migrate
fi
cd ../../..
cd ~/Documents/Work/Distributed\ Systems/4000/octokart
find . -name "*.pyc" -exec rm -rf {} \;
#git pull $BRANCH
cd octokart
if [ "$2" = "migrate" ]
then
    python manage.py makemigrations
    python manage.py migrate
fi
cd ~/Documents/Repositories/octokart
