import nltk
import gensim
import os
import numpy as np
import json
# import math
import sys
import time
import functools

# make the UKR module visible to Python
ukr_path = '/home/disk2/speed/evelin.amorim/Documents/UFMG/python-ukr'
lib_path = os.path.abspath(os.path.join(ukr_path, 'src_naive'))
sys.path.append(lib_path)

import ukr


class Document:

    def __init__(self, docType='average', docExt='json',
                 textField='', targetField=[], docLen=None, writeDocs=False):
        self.docType = docType
        self.docExt = docExt
        # which is text field if a json file is given
        self.textField = textField
        # which target (sentiment aspects to collect) to pick
        self.targetField = targetField
        # for each target field collect its values
        self.target = {}
        if docLen is not None:
            self.docLen = int(docLen)
        else:
            self.docLen = None
        self.__writeDocs = writeDocs

    def read_doc(self, fileName):
        if (self.docExt == 'json'):
            data = json.loads(open(fileName).read())
            data_list = []
            i = 0
            for e in data:
                data_list.append(e[self.textField])
                for t in self.targetField:
                    # print("-->",fileName,i,e[t])
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
                    print(i, os.path.join(subdir, f))
                    strDoc = self.read_doc(os.path.join(subdir, f))
                    docVec = self.build_document(strDoc, model)
                    docList.append(docVec)
                    i = i + 1
        else:
            doc_text = self.read_doc(dirDoc)
            for e in doc_text:
                if self.__writeDocs:
                    fd_doc = open("docs%d.txt" % i, "w")
                print(i)
                docVec = self.build_document(e, model)
                if docVec is not None:
                    nDocVec = len(docVec)
                    # print(">>", docVec[0])
                    # print(docVec, nDocVec)
                if self.__writeDocs and docVec is not None:
                    for j in range(nDocVec):
                        fd_doc.write(functools.reduce(lambda x,y:str(x) + ','
                                                      + str(y), docVec[j]))
                        fd_doc.write('\n')
                    # fd_doc.write(str(docVec[j]))
                    # fd_doc.write('\n')
                docList.append(docVec)
                i = i + 1
                if self.__writeDocs:
                    fd_doc.close()
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
        # return docWordList

        if (len(docWordList) > 0):
            docWordList = np.array(docWordList)
            if self.docType == 'average':
                docWord = self.average_vec(docWordList)
                # simple average or average ber axis?
                # print(len(docWord))
            elif self.docType == 'ps':
                # ps: principal surfaces
                docWord = self.word2ps(docWordList)
            return docWord

    def average_vec(self, vecList):
        m = np.mean(vecList, axis=0)

        return m

    def word2ps(self, vecList):
        # max_iter = 5000
        max_iter = 100
        q = 2
        kernel = ukr.gaussian
        lko_cv = 1
        metric = 'L2'
        nrows = len(vecList)
        if nrows > self.docLen:
            tm = time.time()
            u = ukr.UKR(n_components=q, kernel=kernel, n_iter=max_iter,
                        lko_cv=lko_cv, metric=metric, verbose=False)

            u.fit_transform(vecList)

            embeddings = u.embeddings[0].embedding_
            rangeEmbeddings = list(range(self.docLen, nrows))
            embeddings = np.delete(embeddings, rangeEmbeddings, 0)
            # print(embeddings.shape)

            print('UKR training took %2f seconds' % (time.time() - tm))
            return embeddings.reshape((self.docLen*q,))
        else:
            return None
