import nltk
import gensim
import os
import numpy as np
import json


class Document:

    def __init__(self, testType='average', docType='json',
                 textField='', targetField=[]):
        self.testType = testType
        self.docType = docType
        # which is text field if a json file is given
        self.textField = textField
        # which target (sentiment aspects to collect) to pick
        self.targetField = targetField
        # for each target field collect its values
        self.target = {}

    def read_doc(self, fileName):
        if (self.docType == 'json'):
            data = json.loads(open(fileName).read())
            data_list = []
            i = 0
            for e in data:
                data_list.append(e[self.textField])
                for t in self.targetField:
                    if t in self.target:
                        self.target[t].append((i, e[t]))
                    else:
                        self.target[t] = (i, e[t])
                i = i+1
            return data_list

    def run(self, modelFile, dirDoc):

        model = gensim.models.Word2Vec.load_word2vec_format(modelFile,
                                                            binary=True)
        docList = []
        if (os.path.isdir(dirDoc)):
            for subdir, dirs, files in os.walk(dirDoc):
                for f in files:
                    strDoc = self.read_doc(os.path.join(subdir, f))
                    docVec = self.build_document(strDoc, model)
                    docList.append(docVec)
        else:
            doc_text = self.read_doc(dirDoc)
            for e in doc_text:
                docVec = self.build_document(e, model)
                docList.append(docVec)
        return docList

    def build_document(self, strDoc, model):
        """
        Given one document, the method transform it in
        a vector according to the object type.
        """
        # tokenize document
        # nao posso representar o documento assim..tem que ser dicionario
        tokenList = nltk.tokenize.word_tokenize(strDoc)
        docWordList = []
        for t in tokenList:
            if t.lower() in model:
                docWordList.append(model[t.lower()])
        docWordList = np.array(docWordList)

        if self.testType == 'average':
            docWord = self.average_vec(docWordList)
            # simple average or average ber axis?
            # print(len(docWord))
        return docWord

    def average_vec(self, vecList):
        # print(len(vecList))
        return np.mean(vecList, axis=0)
