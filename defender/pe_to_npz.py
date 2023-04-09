import os
import gzip
import json
import pickle
import numpy as np
# import pandas as pd
# imports
import _pickle as cPickle
from scipy import sparse
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from copy import deepcopy

import lief
# import pandas as pd
from defender.models.attribute_extractor import *
import sys
import os


def usage():
  print("Usage: python pe_to_npz.py <DIRECTORY OF EITHER MALWARE OR GOODWARE FILES> -<b/m> <OUTPUT_FILE_NAME>")
  print("Pass in either an either Malware folder OR entire Goodware Folder, since it will be easier to deal with")
  print()
  sys.exit()

if __name__ == "__main__":
  if len(sys.argv) != 4:
    usage()

  directory_of_files = sys.argv[1]
  output_file = sys.argv[3]
  label = sys.argv[2]
  if label =="-b" : label = 0
  elif label =="-m" : label = 1
  else:
    print("Specify benign or malware properly")
    sys.exit()

  arr_of_features = []

# gw1/0 gw2/1
  X_train = []
  y_train = []
  print("Starting to go through the files")

  for path, subdirs, files in os.walk(directory_of_files):
    for name in files:
      file_name = os.path.join(path, name)

      print('processing', file_name)
      with open(file_name, 'rb') as file:
        file_data = file.read()
        try:
          #file_data_features = PEAttributeExtractor(file_data).extract()
          file_data_features = CustomExtractor(file_data).custom_feature_vector()
          X_train.append(file_data_features)
          y_train.append(label)
          #file_data_features.update({"label": label})
          
          #arr_of_features.append(file_data_features)
        except Exception as inst:
          print(repr(inst))
          print("************************************An exception occurred")

  print("Finished processing all the files")


  ##
#  fp = gzip.open(output_file,'wb')
#  cPickle.dump(arr_of_features,fp)
#  fp.close()
  X_train = np.array(X_train)
  y_train = np.array(y_train)
  print("Shape of X_train = ", X_train.shape)
  print("Shape of y_train = ", y_train.shape)
  np.savez(output_file, x=X_train, y=y_train)
