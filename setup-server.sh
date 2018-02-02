#pull from GitHub
git pull

#install requirements
while read line; do
	pip install $line
done <requirements.txt