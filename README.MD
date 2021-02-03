# GenSci
### Usage:
Install Python 3.8.5 or greater, you can do it via pyenv https://github.com/pyenv/pyenv#installation and virtualenv
```commandline
pyenv install 3.8.5
pyenv virtualenv 3.8.5 gensci
```
Activate the virtualenv
```commandline
pyenv activate gensci
```
Clone the project
```commandline
git clone git@github.com:PHedro/GenSci.git
```
Go to the project folder (the one where you can find the README file)
```commandline
cd /path/to/project/ 
```
Install the project requirements (remember to activate the virtualenv)
```commandline
pip install -r requirements.txt
```
This will install the following dependencies: 
```commandline
Django==2.2.17
django-filter==2.4.0
```

Run the migrations, this will also create the sqlite database 
```commandline
python manage.py migrate 
```
Run the server
```commandline
python manage.py runserver 
```
