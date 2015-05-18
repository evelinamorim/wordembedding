from document import Document
from sklearn.linear_model import LinearRegression

# 'easeOfUse', 'satisfaction','effectiveness'


class Train:

    def __init__(self, textField='', targetFields=[],):
        self.__doc = Document(textField=textField, targetFields=targetFields)
        # a model for each type of target field
        self.__model = {}
        self.ml = mlModel #machine learning model object to train

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
                X.append(docList[idoc])
                y.append(y_value)
                # treinar com a ordem dos valores construidos
