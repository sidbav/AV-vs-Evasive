from copy import deepcopy
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class ImgMal():

    # numerical attributes
    NUMERICAL_ATTRIBUTES = [
        'string_paths', 'string_urls', 'string_registry', 'string_MZ', 'size',
        'virtual_size', 'has_debug', 'imports', 'exports', 'has_relocations',
        'has_resources', 'has_signature', 'has_tls', 'symbols', 'timestamp',
        'numberof_sections', 'major_image_version', 'minor_image_version',
        'major_linker_version', 'minor_linker_version', 'major_operating_system_version',
        'minor_operating_system_version', 'major_subsystem_version',
        'minor_subsystem_version', 'sizeof_code', 'sizeof_headers', 'sizeof_heap_commit'
    ]

    # categorical attributes
    CATEGORICAL_ATTRIBUTES = [
        'machine', 'magic'
    ]

    # textual attributes
    TEXTUAL_ATTRIBUTES = ['libraries', 'functions', 'exports_list',
                          'dll_characteristics_list', 'characteristics_list']

    # label
    LABEL = "label"

    # initialize NFS classifier
    def __init__(self,
                categorical_extractor = OneHotEncoder(handle_unknown="ignore"),
                textual_extractor = TfidfVectorizer(max_features=300, token_pattern=r"(?<=\s)(.*?)(?=\s)"),
                # textual_extractor = HashingVectorizer(n_features=50000, token_pattern=r"(?<=\s)(.*?)(?=\s)"),
                feature_scaler = MinMaxScaler(),
#                 feature_scaler = MaxAbsScaler(),
                classifier = RandomForestClassifier(n_estimators=100)):
        self.base_categorical_extractor = categorical_extractor
        self.base_textual_extractor = textual_extractor
        self.base_feature_scaler = feature_scaler
        self.base_classifier = classifier

    # append features to original features list
    def _append_features(self, original_features, appended):
        if original_features:
            for l1, l2 in zip(original_features, appended):
                for i in l2:
                    l1.append(i)
            return(original_features)
        else:
            return appended.tolist()

    # train a categorical extractor
    def _train_categorical_extractor(self, categorical_attributes):
        # initialize categorical extractor
        self.categorical_extractor = deepcopy(self.base_categorical_extractor)
        # train categorical extractor
        self.categorical_extractor.fit(categorical_attributes.values)

    # transform categorical attributes into features
    def _transform_categorical_attributes(self, categorical_attributes):
        # transform categorical attributes using categorical extractor
        cat_features = self.categorical_extractor.transform(categorical_attributes.values.tolist()).toarray()
        # return categorical features
        return cat_features.tolist()

    # train a textual extractor
    def _train_textual_extractor(self, textual_attributes):
        # initialize textual extractors
        self.textual_extractors = {}
        # train feature extractor for each textual attribute
        for att in self.TEXTUAL_ATTRIBUTES:
            # initialize textual extractors
            self.textual_extractors[att] = deepcopy(self.base_textual_extractor)
            # train textual extractor
            self.textual_extractors[att].fit(textual_attributes[att].values)

    # transform textual extractor
    def _transform_textual_attributes(self, textual_attributes):
        # initialize features
        textual_features = None
        # extract features from each textual attribute
        for att in self.TEXTUAL_ATTRIBUTES:
            # train textual extractor
            att_features = self.textual_extractors[att].transform(textual_attributes[att].values)
            # transform into array (when it is an sparse matrix)
            att_features = att_features.toarray()
            # append textual features
            textual_features = self._append_features(textual_features, att_features)
        return textual_features

    # train feature scaler
    def _train_feature_scaler(self, features):
        # initialize feature scaler
        self.feature_scaler = deepcopy(self.base_feature_scaler)
        # train feature scaler
        self.feature_scaler.fit(features)

    # transform features using feature scaler
    def _transform_feature_scaler(self, features):
        return self.feature_scaler.transform(features)

    # fit classifier using raw input
    def fit(self, train_data):
        # get labels
        train_labels = train_data[self.LABEL]
        # delete label column
        del train_data[self.LABEL]
        # initialize train_features with numerical ones
        train_features = train_data[self.NUMERICAL_ATTRIBUTES].values.tolist()

        print("Training categorical features...")
        # train categorical extractor
        self._train_categorical_extractor(train_data[self.CATEGORICAL_ATTRIBUTES])
        # transform categorical data
        cat_train_features = self._transform_categorical_attributes(train_data[self.CATEGORICAL_ATTRIBUTES])
        # append categorical_features to train_features
        train_features = self._append_features(train_features, cat_train_features)

        print("Training textual features...")
        # train textual extractor
        self._train_textual_extractor(train_data[self.TEXTUAL_ATTRIBUTES])
        # transform textual data
        tex_train_features = self._transform_textual_attributes(train_data[self.TEXTUAL_ATTRIBUTES])
        # append textual_features to train_features
        train_features = self._append_features(train_features, tex_train_features)

        print("Normalizing features...")
        # train feature normalizer
        self._train_feature_scaler(train_features)
        # transform features
        train_features = self._transform_feature_scaler(train_features)

        print("Returning Features...")
        # train classifier
        return (train_features, train_labels)
    
    def train_model(self,train_generator,epoch=10):
        hist = model.fit_generator(
            train_generator,
            steps_per_epoch=math.ceil(train_generator.samples//64),
            epochs=epoch,
            #use_multiprocessing=True, 
            workers=8
        )
    
    def train_transform_img(self,train_features,train_labels,out_path='F:/ML_Cyberspace/Ember_Images/'):
        train_features=train_features*255
        train_labels = np.array(train_labels, dtype=np.int8)
        for x in range(X.shape[0]):
            h,w= 32,32
            img=np.zeros((h,w,3),dtype=np.uint8)
            instance=np.array(X[x,:-1],dtype=np.uint8)
            instance=np.pad(instance, (29, 29), 'constant')
            array = np.reshape(instance, (h, w))
            img[:,:,0]=array
            img[:,:,1]=np.flip(array,0)
            img[:,:,2]=np.flip(array,1)
            data = im.fromarray(img,mode="RGB")
            data.save(out_path+str(Y[x])+'/'+str(x)+'.png',quality=95)

    def _extract_features(self,data):
        # initialize features with numerical ones
        features = data[self.NUMERICAL_ATTRIBUTES].values.tolist()

        #print("Getting categorical features...")
        # transform categorical data
        cat_features = self._transform_categorical_attributes(data[self.CATEGORICAL_ATTRIBUTES])
        # append categorical_features to features
        features = self._append_features(features, cat_features)

        #print("Getting textual features...")
        # transform textual data
        tex_features = self._transform_textual_attributes(data[self.TEXTUAL_ATTRIBUTES])
        # append textual_features to features
        features = self._append_features(features, tex_features)

        #print("Normalizing features...")
        # transform features
        features = self._transform_feature_scaler(features)
        #print("Done")

        # return features
        return(features)
    
    def predict_threshold(self,test_data, threshold=0.75):
        # extract features
        test_features = self._extract_features(test_data)
        #Transforming Data into 0-255 range
        test_features=test_features*255
        #print("Predicting classes (threshold = {})...".format(threshold), flush=True)
        ## Transformation into Image
        pred = []
        if (test_features.ndim<2):
            h,w= 32,32
            img=np.zeros((h,w,3),dtype=np.uint8)
            instance=np.array(test_features[0,:-1],dtype=np.uint8)
            instance=np.pad(instance, (29, 29), 'constant')
            array = np.reshape(instance, (h, w))
            img[:,:,0]=array
            img[:,:,1]=np.flip(array,0)
            img[:,:,2]=np.flip(array,1)
            data = np.expand_dims(img, axis=0)
            prob = self.base_classifier.predict(data)
            pred.append(int(prob[0] >= threshold))
        else:
            for x in range(test_features.shape[0]):
                h,w= 32,32
                img=np.zeros((h,w,3),dtype=np.uint8)
                instance=np.array(test_features[x,:-1],dtype=np.uint8)
                instance=np.pad(instance, (29, 29), 'constant')
                array = np.reshape(instance, (h, w))
                img[:,:,0]=array
                img[:,:,1]=np.flip(array,0)
                img[:,:,2]=np.flip(array,1)
                data = np.expand_dims(img, axis=0)
                prob = self.base_classifier.predict(data)
                pred.append(int(prob[0] >= threshold))
        # return prediction
        return pred
    
    def predict_threshold_prob(self,test_data, threshold=0.75):
        # extract features
        test_features = self._extract_features(test_data)
        #Transforming Data into 0-255 range
        test_features=test_features*255
        #print("Predicting classes (threshold = {})...".format(threshold), flush=True)
        ## Transformation into Image
        pred = []
        if (test_features.ndim<2):
            h,w= 32,32
            img=np.zeros((h,w,3),dtype=np.uint8)
            instance=np.array(test_features[0,:-1],dtype=np.uint8)
            instance=np.pad(instance, (29, 29), 'constant')
            array = np.reshape(instance, (h, w))
            img[:,:,0]=array
            img[:,:,1]=np.flip(array,0)
            img[:,:,2]=np.flip(array,1)
            data = np.expand_dims(img, axis=0)
            prob = self.base_classifier.predict(data)
            pred.append(prob[0])
        else:
            for x in range(test_features.shape[0]):
                h,w= 32,32
                img=np.zeros((h,w,3),dtype=np.uint8)
                instance=np.array(test_features[x,:-1],dtype=np.uint8)
                instance=np.pad(instance, (29, 29), 'constant')
                array = np.reshape(instance, (h, w))
                img[:,:,0]=array
                img[:,:,1]=np.flip(array,0)
                img[:,:,2]=np.flip(array,1)
                data = np.expand_dims(img, axis=0)
                prob = self.base_classifier.predict(data)
                pred.append(prob[0])
        return pred