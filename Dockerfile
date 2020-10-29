# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY uptimerobot_exporter/ uptimerobot_exporter

# command to run on container start
CMD [ "python", "-m", "uptimerobot_exporter" ] 