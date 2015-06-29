from document import Document
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

    def __init__(self, testType='average', textField='', targetFields=[],
                 modelType=None, docType='json'):
        self.__doc = Document(testType=testType, textField=textField,
                              targetField=targetFields,
                              docType=docType)
        self.__testType = testType
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
                    for e in docList[idoc]:
                        X.append(e)
                        # print(docList[idoc])
                        y.append(y_value)
            print(t, max(y))
            # print("-->", X[0].shape)
            # treinar com a ordem dos valores construidos
            X = np.asarray(X)
            y = np.array(y)
            # print(X.shape, y.shape)
            # print(type(X), type(y))
            # print(X[0][1], y.shape)
            # print(X[1].shape, y.shape)
            self.__model[t].fit(X, y)
            # self.__model[t] = sm.OLS(y, X)
            # res = self.__model[t].fit()
            # print(res.summary())
            # plt.hist(res.resid_pearson)
            # plt.ylabel('Count')
            # plt.xlabel('Normalized Residuals')
            # plt.savefig("hist_%s.png" % t)

    def write_models(self, dirOut):
        for t in self.__model:
            fileModel = os.path.join(dirOut, "%s_%s_%s.pkl" % (t,
                                                               self.__testType,
                                                               self.__modelType)
                                     )
            joblib.dump(self.__model[t], fileModel)

if __name__ == "__main__":
    trainObj = Train(testType='linearregression',
                     textField='reviewComment',
                     targetFields=['easeOfUse',
                                   'satisfaction',
                                   'effectiveness'],
                     modelType='LinearRegression')
    trainObj.run('/scratch2/evelin.amorim/WebMD/vectors_webmd_cons.bin',
                 '/scratch2/evelin.amorim/WebMD/train_drugs_reviews.json')
    trainObj.write_models('out/')
