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


        resp = {
            'result': None,
            'model1' : {
                0: None,
                1: None
            },
            'model2': {
                0: None,
                1: None,
            },
            'final_model': {
                0: None,
                1: None,
            }
        }

        try:
            custom_ext = CustomExtractor(bytez)
            attributes = custom_ext.custom_attribute_extractor()
            model1 = app.config['model1']
            model2 = app.config['model2']

            result_prob1 = custom_ext.custom_predict_with_threshold(model1)
            result = 0

            print('LABEL PROB MODEL 1= ', result_prob1)
            resp['model1'][0] = result_prob1[0][0]
            resp['model1'][1] = result_prob1[0][1]
            resp['final_model'][0] = result_prob1[0][0]
            resp['final_model'][1] = result_prob1[0][1]

            if result_prob1[0][0] >= 0.6 and result_prob1[0][0] <= 0.64:

                model2 = app.config['model2']
                result_prob2 = custom_ext.custom_predict_with_threshold(model2)
                if result_prob2[0][0] < 0.47:
                    result = 1

                print('LABEL PROB MODEL 2=', result_prob2)

                resp['model2'][0] = result_prob2[0][0]
                resp['model2'][1] = result_prob2[0][1]
                resp['final_model'][0] = result_prob2[0][0]
                resp['final_model'][1] = result_prob2[0][1]

            elif result_prob1[0][0] < 0.61:
                result = 1

            resp['result'] = result
            print('LABEL = ', result)
        except (lief.bad_format, lief.read_out_of_bound) as e:
            print("Error:", e)
            result = 1

        if not isinstance(result, int) or result not in {0, 1}:
            resp = jsonify({'error': 'unexpected model result (not in [0,1])'})
            resp.status_code = 500  # Internal Server Error
            return resp

        resp = jsonify(resp)
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
