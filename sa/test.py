from document import Document
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
import os
import numpy as np
from config import Config


class Test:

    def __init__(self, textField='', targetFields=[], docType=None,
                 modelType=None, docLen=None):
        self.__doc = Document(docType=docType, textField=textField,
                              targetField=targetFields, docLen=docLen)
        # a model for each type of target field
        self.__model = {}
        self.__modelType = modelType
        self.__docType = docType
        self.__docLen = docLen

    def run(self, wordModelFile, docTestFile, dirOut=''):
        """
        Test a linear regression
        """
        docList = self.__doc.run(wordModelFile,
                                 docTestFile)
        for t in self.__doc.target:
            fd_pred = open("pred%s.txt" % t, "w")

            y = []
            X = []
            if (self.__docLen is None):
                fileNameModel = "%s_%s_%s.pkl" % (t, self.__docType,
                                                  self.__modelType)
            else:
                fileNameModel = "%s_%s_%s_%s.pkl" % (t, self.__docType,
                                                     self.__modelType,
                                                     self.__docLen)

            fileModel = os.path.join(dirOut, fileNameModel)
            self.__model[t] = joblib.load(fileModel)
            pred_final = []
            for (idoc, y_value) in self.__doc.target[t]:
                # print(t)
                if (docList[idoc] is not None):
                    X.append(docList[idoc])
                    # print(docList[idoc])
                    y.append(y_value)
                    pred = self.__model[t].predict(docList[idoc])
                    pred_final_doc = np.mean(pred)
                    pred_final.append(pred_final_doc)
                    fd_pred.write("%d %f\n" % (idoc,pred_final_doc))
                    # print(docList[idoc],y_value,pred)
                    # print(np.mean(pred))
            fd_pred.close()
            print("Category ", t, " Error: ", mean_squared_error(y, pred_final))

if __name__ == '__main__':
    cfgObj = Config()
    cfgObj.read('test.cfg')

    docType = cfgObj.get_field('docType')
    textField = cfgObj.get_field('textField')
    targetFields = cfgObj.get_field('targetFields')
    modelType = cfgObj.get_field('modelType')
    docLen = cfgObj.get_field('docLen')

    doc = Test(textField=textField, targetFields=targetFields,
               docType=docType, modelType=modelType, docLen=docLen)

    vectorModelFile = cfgObj.get_field('vectorModelFile')
    trainTextFile = cfgObj.get_field('trainTextFile')
    modelDir = cfgObj.get_field('modelDir')

    docList = doc.run(vectorModelFile, trainTextFile, dirOut=modelDir)
