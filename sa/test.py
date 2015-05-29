from document import Document
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
import os


class Test:

    def __init__(self, textField='', targetFields=[], modelType=None):
        self.__doc = Document(textField=textField, targetField=targetFields)
        # a model for each type of target field
        self.__model = {}
        self.__modelType = modelType

    def run(self, wordModelFile, docTestFile, dirOut=''):
        """
        Test a linear regression
        """
        docList = self.__doc.run(wordModelFile,
                                 docTestFile)
        for t in self.__doc.target:
            y = []
            X = []
            fileModel = os.path.join(dirOut, "%s_%s.pkl" % (t,
                                                            self.__modelType))
            self.__model[t] = joblib.load(fileModel)
            for (idoc, y_value) in self.__doc.target[t]:
                if (docList[idoc] is not None):
                    X.append(docList[idoc])
                    # print(docList[idoc])
                    y.append(y_value)
            pred = self.__model[t].predict(X)
            print("Category ", t, " Error: ", mean_squared_error(y, pred))

if __name__ == '__main__':
    doc = Test(textField='reviewComment',
               targetFields=['easeOfUse',
                             'satisfaction',
                             'effectiveness'],
               modelType='LinearRegression')
    docList = doc.run('/scratch2/evelin.amorim/WebMD/vectors_webmd_cons.bin',
                      '/scratch2/evelin.amorim/WebMD/test_drugs_reviews.json',
                      dirOut='out')
