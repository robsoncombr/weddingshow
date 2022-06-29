#FROM python:2.7
# decided to use latest to implement websockets
FROM python:latest

# https://stackoverflow.com/questions/48561981/activate-python-virtualenv-in-dockerfile
RUN mkdir /weddingshow
WORKDIR /weddingshow

# removed because it is already docker isolated
# note: if used it is necessary to activate with: source ./env/bin/activate
#RUN pip install virtualenv
#RUN cd /weddingshow; virtualenv env
#RUN cd /weddingshow; ./env/bin/pip install flask flask-wtf flask-sqlalchemy pymongo

# update pip version (usually the one delivered with the image is old)
RUN python -m pip install --upgrade pip

# debug: https://pypi.org/project/ipdb/
RUN pip install ipdb
# flask
RUN pip install flask flask-wtf email_validator flask-sqlalchemy
# flask server side session - https://flask-session.readthedocs.io/en/latest
RUN pip install flask-session
# flask websocket server - https://flask-sock.readthedocs.io/en/latest
RUN pip install flask-sock
# mongodb
#RUN pip install pymongo # I have decided to use MongoEngine instead of pymongo
RUN pip install flask-mongoengine
# api
RUN pip install flask-cors pyjwt
# aws
RUN pip install boto3 awscli

# requirements notes:
# generate project requirements: pip freeze > requirements.txt
# install project requirements: pip install -r requirements.txt

#COPY /nuvial/weddingshow/back-flask/.aws /root

CMD ["python", "run.py"]