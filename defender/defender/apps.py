import lief
# import pandas as pd
from flask import Flask, jsonify, request
from defender.models.attribute_extractor import *
import pefile
import sys

import re
import math
import numpy as np
# import pandas as pd
import ember

def create_app(model1, model2, threshold):
    app = Flask(__name__)
    app.config['model1'] = model1
    app.config['model2'] = model2

    # analyse a sample
    @app.route('/', methods=['POST'])
    def post():
        # curl -XPOST --data-binary @somePEfile http://127.0.0.1:8080/ -H "Content-Type: application/octet-stream"
        if request.headers['Content-Type'] != 'application/octet-stream':
            resp = jsonify({'error': 'expecting application/octet-stream'})
            resp.status_code = 400  # Bad Request
            return resp

        bytez = request.data
        try:
            pe = pefile.PE(data=bytez)
        except:
            resp = jsonify({'error': 'Not PE File!'})
            resp.status_code = 400
            return resp

        try:
            custom_ext = CustomExtractor(bytez)
            attributes = custom_ext.custom_attribute_extractor()
            model1 = app.config['model1']
            model2 = app.config['model2']

            result_prob1 = custom_ext.custom_predict_with_threshold(model1)
            result = 0

            if result_prob1[0][0] >= 0.6 and result_prob1[0][0] <= 0.64:

                model2 = app.config['model2']
                result2_prob = custom_ext.custom_predict_with_threshold(model2)
                if result2_prob[0][0] < 0.47:
                    result = 1

            elif result_prob1[0][0] < 0.61:
                result = 1

            print('LABEL = ', result)
            #print('LABEL PROB = ', result_prob1)
        except (lief.bad_format, lief.read_out_of_bound) as e:
            print("Error:", e)
            result = 1

        if not isinstance(result, int) or result not in {0, 1}:
            resp = jsonify({'error': 'unexpected model result (not in [0,1])'})
            resp.status_code = 500  # Internal Server Error
            return resp

        resp = jsonify({'result': result})#, 'result_proba_0': result_prob1[0][0], 'result_proba_1': result_prob1[0][1]})#, 'result_proba_-1': result_prob[0][2]})
        resp.status_code = 200
        return resp

    # # get the model info
    # @app.route('/model', methods=['GET'])
    # def get_model():
    #     # curl -XGET http://127.0.0.1:8080/model
    #     resp = jsonify(app.config['model'].model_info())
    #     resp.status_code = 200
    #     return resp

    return app
