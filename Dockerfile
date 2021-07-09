#Create a ubuntu base image with python 3 installed.
FROM python:3

#Set the working directory
WORKDIR /usr/src/app

#copy all the files
COPY . .

#Install the dependencies
RUN apt-get -y update
RUN pip3 install flask

#Expose the required port
EXPOSE 5000

#Run the command
CMD ["python3", "./src/app.py"]