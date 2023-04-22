import os
import gzip
import pickle
import envparse
from scipy import sparse
import _pickle as cPickle
from defender.apps import create_app
import keras
import lightgbm as lgb
import joblib

# CUSTOMIZE: import model to be used
from defender.models.ImgMal import ImgMal

def load_gzip_pickle(filename):
    fp = gzip.open(filename,'rb')
    obj = cPickle.load(fp)
    fp.close()
    return obj

if __name__ == "__main__":
    # retrive config values from environment variables
    model_gz_path = envparse.env("DF_MODEL_GZ_PATH", cast=str, default="models/ImgMal_v1.pkl")
    model_thresh = envparse.env("DF_MODEL_THRESH", cast=float, default=0.5)
    model_name = envparse.env("DF_MODEL_NAME", cast=str, default="ImgMal_v1")
    deep_model_name = envparse.env("Deep_DF_MODEL_NAME", cast=str, default="models/My_model")
    lgbm_model_name = envparse.env("LGBM Model", cast=str, default="models/ember_model_2018.txt")
    rf_name = envparse.env("RF Model", cast=str, default="models/random_forest.joblib")
    # model_ball_thresh = envparse.env("DF_MODEL_BALL_THRESH", cast=float, default=0.25)
    # model_max_history = envparse.env("DF_MODEL_HISTORY", cast=int, default=10_000)

    # construct absolute path to ensure the correct model is loaded
    if not model_gz_path.startswith(os.sep):
        model_gz_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), model_gz_path)
        deep_model_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), deep_model_name)
        lgbm_model_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), lgbm_model_name)
        ## Loading the Saved Random Forest Classifer 
        rf_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), rf_name)
    
        
    # CUSTOMIZE: app and model instance
    model = load_gzip_pickle(model_gz_path)
    # model = StatefulNNEmberModel(model_gz_path,
    #                              model_thresh,
    #                              model_ball_thresh,
    #                              model_max_history,
    #                              model_name)
    loaded_rf = joblib.load(rf_name)
    lgbm_model = lgb.Booster(model_file=lgbm_model_name)
    model.base_classifier=keras.models.load_model(deep_model_name)
    

    app = create_app(model, model_thresh,loaded_rf,lgbm_model)

    import sys
    port = 8080

    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

    # curl -XPOST --data-binary @somePEfile http://127.0.0.1:8080/ -H "Content-Type: application/octet-stream"a