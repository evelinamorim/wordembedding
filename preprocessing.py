# -*- coding: utf-8 -*-
#author: evelin amorim

#the preprocessing class perform:
# 1) Read wikipedia 
#    1.1) for each body in wikipedia
#       1.1.1)filter non alphanumeric, allowing mid-token 
#       symbols: apostrophes, hyphens, commas, and periods
#       1.1.2) text are lowercased
#       1.1.3) Duplicates are removed
#       1.1.4) Sentences with less than 5 tokens were removed

import sys
from mw import xml_dump
from gensim.models import word2vec
import sys
import re
import codecs

# [^A-Za-z0-9'-\.]
class PreProcess:

    def __init__(self,train_type='wikipedia'):
        self.__train_type = train_type
        self.input_train = None

    def read_train(self,file_name):
        """
        @input file_name string: The file name for the 
	           training input
        """

        if (self.__train_type=='wikipedia'):
            self.read_wikipedia(file_name)
        elif (self.__train_type=='plain'):
            #plain text to train
            self.input_train = self.read_plain(file_name)
        else:
            print("Error: Train type not supported")
            sys.exit(0)

    def read_plain(self,file_name):
        """
        Read plain text to train
        TODO: generalizar para outros diferentes do text8 e depois 
        passar pelo pre-processamento descrito no artigo
        """
        sentences = word2vec.Text8Corpus(file_name)
        return sentences

    def read_wikipedia(self,file_name):
        """
        Read and pre-process wikipedia dump file

        @input file_name string: The file name for the 
	           training input
        """
        dump = xml_dump.Iterator.from_file(codecs.open(file_name,"r","utf-8"))

        i = 1
        #pages that dont need to be processed
        redirect_page = re.compile('#REDIRECT')
        for page in dump:
            print("*******************************")
            for revision in page:
                if (not(redirect_page.match(revision.text))):
                    print("{0} ".format( revision.text.encode('UTF-8')))
                    print("{0} ".format(page.title))

            if (i==10): break
            print()
            i = i+1

    def write_wikipedia():
        """
         Write de preprocessed wikipedia
        """
        pass


if __name__ == "__main__":
   pp = PreProcess()
   train_file = sys.argv[1]
   pp.read_train(train_file)
