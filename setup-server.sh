#stop app
supervisorctl stop flaskapp

#set up venv
#virtualenv -p python3 env
source env/bin/activate

#install requirements
while read line; do
	pip3 install $line
done <requirements.txt

#start app
supervisorctl start flaskapp
