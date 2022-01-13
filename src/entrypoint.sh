# copy the config file from src folder to config folder
mkdir -p ./config
cp /app/config.yaml ./config/config.yaml

# command to run on container start
#CMD [ "python", "./fileOrganizer.py" ]
#cmd /bin/sh

# show log and wait
tail -f --retry /app/ 2> /dev/null &
wait