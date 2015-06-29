import nltk
import gensim
import os
import numpy as np
import json
# import math
import sys
import time


# make the UKR module visible to Python
ukr_path = '/home/disk2/speed/evelin.amorim/Documents/UFMG/python-ukr'
lib_path = os.path.abspath(os.path.join(ukr_path, 'src_naive'))
sys.path.append(lib_path)

import ukr


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
                        self.target[t] = [(i, e[t])]
                i = i+1
            return data_list

    def run(self, modelFile, dirDoc):

        model = gensim.models.Word2Vec.load_word2vec_format(modelFile,
                                                            binary=True)
        docList = []
        i = 1
        if (os.path.isdir(dirDoc)):
            for subdir, dirs, files in os.walk(dirDoc):
                for f in files:
                    print(i)
                    strDoc = self.read_doc(os.path.join(subdir, f))
                    docVec = self.build_document(strDoc, model)
                    docList.append(docVec)
                    i = i + 1
        else:
            doc_text = self.read_doc(dirDoc)
            for e in doc_text:
                print(i)
                docVec = self.build_document(e, model)
                docList.append(docVec)
                i = i + 1
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
        if (len(docWordList) > 0):
            docWordList = np.array(docWordList)
            if self.testType == 'average':
                docWord = self.average_vec(docWordList)
                # simple average or average ber axis?
                # print(len(docWord))
            elif self.testType == 'linearregression':
                docWord = self.word2linearregression(docWordList)
            return docWord

    def average_vec(self, vecList):
        # print(len(vecList))
        m = np.mean(vecList, axis=0)

        # print(m)  # numpy.ndarray
        return m

    def word2linearregression(self, vecList):
        # max_iter = 5000
        max_iter = 100
        q = 2
        kernel = ukr.gaussian
        lko_cv = 1
        metric = 'L2'

        tm = time.time()
        u = ukr.UKR(n_components=q, kernel=kernel, n_iter=max_iter,
                    lko_cv=lko_cv, metric=metric, verbose=False)
        mani = u.fit_transform(vecList)
        i = 0
        # print(u.embeddings[0].embedding_.shape)
        embeddings = u.embeddings[0].embedding_
        e_array = []
        for e in embeddings:
            # print(e.shape, e_array.shape)
            # print("-->", e, e_array)
            e_array.append(e)
            # print("==>", e_array)
            # if (i == 2):
            #    print(">>>", np.asarray(e_array), np.asarray(e_array).shape)
            #    sys.exit(0)
            i = i+1
        e_array = np.asarray(e_array)
        # print(e_array.shape)
        # print(mani.shape)  # numpy.ndarray
        # print(vecList.shape)
        print('UKR training took %2f seconds' % (time.time() - tm))
        # return mani
        return e_array
