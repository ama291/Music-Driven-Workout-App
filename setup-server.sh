#install requirements
while read line; do
	pip3 install $line
done <requirements.txt