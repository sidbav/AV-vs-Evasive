FROM python@sha256:ad164c2ec67834a0876c96e2ad63b2c7dfbbd784b4879ba6cca789b5e9dccd59

#############################
# INSTALL PYTHON DEPENDENCIES
#############################

# install git for pip install git+https://
RUN apt-get -o Acquire::Max-FutureTime=100000 update \
 && apt-get install -y --no-install-recommends build-essential git

# create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# copy and install python requirements + ember from github
COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt \
 && pip install --no-cache-dir git+https://github.com/elastic/ember.git

#############################
# REBASE & DEPLOY CODE
#############################

# rebase to make a smaller image
FROM python:3.9.16-slim

# required libgomp1 for ember
RUN apt-get -o Acquire::Max-FutureTime=100000 update \
    && apt-get -y --no-install-recommends install \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# copy python virtual env (all dependencies) from previous image
COPY --from=0 /opt/venv /opt/venv

# copy defender code to /opt/defender/defender
COPY defender /opt/defender/defender

#############################
# SETUP ENVIRONMENT
#############################

# open port 8080
EXPOSE 8080

# add a defender user and switch user
RUN groupadd -r defender && useradd --no-log-init -r -g defender defender
# TODO: UNCOMMENT THIS BELOW AND REBUILT BEFORE SUBMITTING TO PREVENT ACCESS
RUN rm /bin/*
USER defender

# change working directory
WORKDIR /opt/defender/

# update environmental variables
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/defender"

# one may tune model file / threshold / name via environmental variables
# ENV DF_MODEL_GZ_PATH models/NFS_V3.pkl.gz
# ENV DF_MODEL_GZ_PATH models/NFS_21_ALL_hash_50000_WITH_TEST.pkl
# ENV DF_MODEL_GZ_PATH models/NFS_21_ALL_hash_50000_WITH_MLSEC19.pkl
ENV DF_MODEL_GZ_PATH models/NFS_21_ALL_hash_50000_WITH_MLSEC20.pkl
ENV DF_MODEL_JOBLIB_PATH models/something.joblib
#ENV DF_MODEL_PKL_PATH models/RFC_unkown_removed_300_25.pkl
ENV DF_MODEL1_PKL_PATH models/zoe.pkl
ENV DF_MODEL2_PKL_PATH models/mike.pkl
ENV DF_MODEL3_PKL_PATH models/raffy.pkl
ENV DF_MODEL_THRESH 0.75
ENV DF_MODEL1_THRESH 0.31
ENV DF_MODEL2_THRESH 0.25
ENV DF_MODEL3_THRESH 0.12
# ENV DF_MODEL_THRESH 0.46875
ENV DF_MODEL_NAME NFS_V3

#############################
# RUN CODE
#############################
CMD ["python","-m","defender"]

## TO BUILD IMAGE:
# docker build -t ember .
## TO RUN IMAGE (ENVIRONMENTAL VARIABLES DECLARED ABOVE)
# docker run -itp 8080:8080 ember
## TO RUN IMAGE (OVERRIDE ENVIRONMENTAL VARIABLES DECLARED ABOVE)
# docker run -itp 8080:8080 --env DF_MODEL_GZ_PATH="models/ember_model.txt.gz" --env DF_MODEL_THRESH=0.8336 --env DF_MODEL_NAME=myember ember
