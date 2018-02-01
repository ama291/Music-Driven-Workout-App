#pull from GitHub
git pull

#set up venv
virtualenv -p python3 env
source env/bin/activate

#install requirements
while read line; do
	pip install $line
done <requirements.txt