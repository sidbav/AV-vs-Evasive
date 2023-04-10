import os
import gzip
import pickle
import envparse
import _pickle as cPickle
from defender.apps import create_app
import joblib

# CUSTOMIZE: import model to be used
from defender.models.nfs_model import NeedForSpeedModel

def load_model(model_file_path):
    # model = joblib.load(model_file_path)
    model_file = open(model_file_path,'rb')
    model = pickle.load(model_file)
    model_file.close()

    return model

def load_gzip_pickle(filename):
    fp = gzip.open(filename,'rb')
    obj = cPickle.load(fp)
    fp.close()
    return obj

if __name__ == "__main__":
    # retrive config values from environment variables
    model_gz_path = envparse.env("DF_MODEL_GZ_PATH", cast=str, default="models/NFS_V3.pkl.gz")
    model_thresh = envparse.env("DF_MODEL_THRESH", cast=float, default=0.7)
    model_name = envparse.env("DF_MODEL_NAME", cast=str, default="NFS_V3")

    model_joblib_path = envparse.env("DF_MODEL_JOBLIB_PATH", cast=str, default="models/RFC_V1.joblib")
    model_pkl_path1 = envparse.env("DF_MODEL1_PKL_PATH", cast=str, default="models/RFC_V1.pkl")
    model_pkl_path2 = envparse.env("DF_MODEL2_PKL_PATH", cast=str, default="models/RFC_V1.pkl")
    # model_ball_thresh = envparse.env("DF_MODEL_BALL_THRESH", cast=float, default=0.25)
    # model_max_history = envparse.env("DF_MODEL_HISTORY", cast=int, default=10_000)

    # construct absolute path to ensure the correct model is loaded
    if not model_pkl_path1.startswith(os.sep):
        model_pkl_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), model_pkl_path1)
    if not model_pkl_path2.startswith(os.sep):
        model_pkl_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), model_pkl_path2)

    # CUSTOMIZE: app and model instance
    # with open(model_joblib_path, 'rb') as model_data:
    model1 = load_gzip_pickle(model_pkl_path1)
    model2 = load_gzip_pickle(model_pkl_path2)
    # model = StatefulNNEmberModel(model_gz_path,
    #                              model_thresh,
    #                              model_ball_thresh,
    #                              model_max_history,
    #                              model_name)
    model1.verbose = 0
    model2.verbose = 0

    app = create_app(model1, model2, model_thresh)

    print("Server started!")
    import sys
    port = int(sys.argv[1]) if len(sys.argv) == 2 else 8080

    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

    # curl -XPOST --data-binary @somePEfile http://127.0.0.1:8080/ -H "Content-Type: application/octet-stream"
