#FROM python:2.7
# decided to use latest to implement websockets
FROM python:latest
# https://stackoverflow.com/questions/48561981/activate-python-virtualenv-in-dockerfile
RUN mkdir /weddingshow

# removed because it is already docker isolated
# note: if used it is necessary to activate with: source ./env/bin/activate
#RUN pip install virtualenv
#RUN cd /weddingshow; virtualenv env
#RUN cd /weddingshow; ./env/bin/pip install flask flask-wtf flask-sqlalchemy pymongo

# debug: https://pypi.org/project/ipdb/
RUN pip install ipdb
# flask
RUN pip install flask flask-wtf email_validator flask-sqlalchemy
# websocket
RUN pip install flask-sock
# mongodb
RUN pip install pymongo
# aws
RUN pip install boto3

# requirements notes:
# generate project requirements: pip freeze > requirements.txt
# install project requirements: pip install -r requirements.txt

WORKDIR /weddingshow

CMD ["python", "run.py"]