import lief
import pandas as pd
from flask import Flask, jsonify, request,render_template
from defender.models.attribute_extractor import PEAttributeExtractor
from defender.models.PE_extract_ember import predict_sample



def create_app(model, threshold, loaded_rf, lgbm_model):
    app = Flask(__name__)
    app.config['model'] = model
    
    ### Herer
    ### Here !!!

    @app.route('/check')
    def hello():
        """ Main page of the app. """
        print("Server is Live !!!")
        X="Server is Live !!!"
        return X
        
    # @app.route('/home')
    # def hey():
    #     """ Main page of the app. """
    #     return render_template('main.html')

    #analyse a sample
    @app.route('/', methods=['POST'])
    def post():
        # curl -XPOST --data-binary @somePEfile http://127.0.0.1:80/ -H "Content-Type: application/octet-stream"
        if request.headers['Content-Type'] != 'application/octet-stream':
            resp = jsonify({'error': 'expecting application/octet-stream'})
            resp.status_code = 400  # Bad Request
            return resp

        bytez = request.data
        Loop_value=[]
        try:
            pred=predict_sample(lgbm_model, bytez)
            lgbm_pred = pred
            print('lgbm prediction', pred)
            # initialize feature extractor with bytez
            pe_att_ext = PEAttributeExtractor(bytez)
            # extract PE attributes
            atts = pe_att_ext.extract()
            # transform into a dataframe
            atts = pd.DataFrame([atts])
            model = app.config['model']
            # query the model
            pred_imgmal=model.predict_threshold_prob(atts,threshold = threshold)[0][0]
            print('image mal pred', pred_imgmal)
        except:
            pred_imgmal = -1
        Loop_value.append([pred,pred_imgmal])
        final_answer=loaded_rf.predict_proba(Loop_value)
        ## Predicting 
        print('final answer', final_answer)
        result=int(final_answer[0][1]>=threshold)
        print('LABEL = ', result)
        print(threshold)

        if not isinstance(result, int) or result not in {0, 1}:
            resp = jsonify({'error': 'unexpected model result (not in [0,1])'})
            resp.status_code = 500  # Internal Server Error
            return resp

        resp = jsonify({'1lgbm_pred': lgbm_pred, '2pred_imgmal': str(pred_imgmal), '3final_RFC_pred0': final_answer[0][0],
                        '3final_RFC_pred1':final_answer[0][1], 'result': result})
        resp.status_code = 200
        return resp

    #get the model info
    @app.route('/model', methods=['GET'])
    def get_model():
        # curl -XGET http://127.0.0.1:80/model
        resp = jsonify("Guess What it could be ?")
        resp.status_code = 200
        return resp

    return app
