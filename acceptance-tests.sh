localAPI="http://127.0.0.1:5000"

workout=$(curl --data "userid=1&equipment=Body Only,Kettlebells&duration=50&difficulty=Intermediate&categories=Cardio,Stretching&key=SoftCon2018" ${localAPI}/api/workouts/getworkout/)

echo ${workout}

curl --data "userid=1&workout=${workout}&key=SoftCon2018" ${localAPI}/api/workouts/startworkout/

