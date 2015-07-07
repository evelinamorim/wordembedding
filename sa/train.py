from document import Document
from config import Config
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.externals import joblib
import os
import numpy as np
# import statsmodels.api as sm
import matplotlib

matplotlib.use('Agg')

# import matplotlib.pyplot as plt
# 'easeOfUse', 'satisfaction','effectiveness'


class Train:

    def __init__(self, docType='average', textField='', targetFields=[],
                 modelType=None, docExt='json', docLen=None):
        self.__doc = Document(docType=docType, textField=textField,
                              targetField=targetFields,
                              docExt=docExt, docLen=docLen)
        self.__docType = docType
        self.__docLen = docLen
        # a model for each type of target field
        self.__model = {}
        self.__modelType = modelType
        # if (modelType is None):
        for t in targetFields:
            if (modelType == 'LinearRegression'):
                self.__model[t] = LinearRegression()
            elif (modelType == 'svm'):
                self.__model[t] = svm.SVC()

    def run(self, wordModelFile, docTrainFile):
        """
        Train a linear regression
        """
        docList = self.__doc.run(wordModelFile,
                                 docTrainFile)
        for t in self.__doc.target:
            y = []
            X = []
            for (idoc, y_value) in self.__doc.target[t]:
                if (docList[idoc] is not None):
                    # for e in docList[idoc]:
                    X.append(docList[idoc])
                    y.append(y_value)
            # print(t, max(y))
            # treinar com a ordem dos valores construidos
            X = np.asarray(X)
            print(X.shape)
            y = np.array(y)
            self.__model[t].fit(X, y)

    def write_models(self, dirOut):
        for t in self.__model:
            fileModelName = ''
            if self.__docLen == None:
                fileModelName = "%s_%s_%s.pkl" % (t, self.__docType,
                                                  self.__modelType)
            else:
                fileModelName = "%s_%s_%s_%s.pkl" % (t, self.__docType,
                                                     self.__modelType,
                                                     self.__docLen)

            fileModel = os.path.join(dirOut,fileModelName)
            joblib.dump(self.__model[t], fileModel)

if __name__ == "__main__":
    cfgObj = Config()

    cfgObj.read('train.cfg')

    docType=cfgObj.get_field('docType')
    textField=cfgObj.get_field('textField')
    targetFields=cfgObj.get_field('targetFields')
    modelType=cfgObj.get_field('modelType')
    docLen=cfgObj.get_field('docLen')

    trainObj = Train(docType=docType, textField=textField,
                     targetFields=targetFields, modelType=modelType,
                     docLen=docLen)

    vectorModelFile=cfgObj.get_field('vectorModelFile')
    trainTextFile=cfgObj.get_field('trainTextFile')
    modelDir=cfgObj.get_field('modelDir')

    trainObj.run(vectorModelFile, trainTextFile)
    trainObj.write_models(modelDir)
