# -*- coding: utf-8 -*-
# author: evelin amorim

# the preprocessing class perform:
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
import re
import codecs
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer

from util import process_wiki_str


# [^A-Za-z0-9'-\.]
class PreProcess:

    def __init__(self, train_type='wikipedia', dir_out=None):
        self.__train_type = train_type
        self.input_train = None
        self.dir_out = dir_out

    def read_train(self, file_name, readraw=True, writesentences=True):
        """
        @input file_name string: The file name for the training input
        @input readraw boolean: read a raw file in order to create
              a file to process_file. If the file are already a plain text
              file, and therefore dont need any special treatment, this
              option can be set to False
        @input writesentences boolean: if the file with the sentences
             separated is already created, then set this to False
        """

        if (self.__train_type == 'plain'):
            # plain text to train
            self.input_train = self.read_plain(file_name)
        else:
            print("Error: Train type not supported")
            sys.exit(0)

    def read_plain(self, file_name):
        """
        Read plain text to train
        TODO: generalizar para outros diferentes do text8 e depois
        passar pelo pre-processamento descrito no artigo
        """
        sentences = word2vec.Text8Corpus(file_name)
        return sentences

    def read_wikipedia(self, file_name):
        """
        Read and pre-process wikipedia dump file

        @input file_name string: The file name for the training input
        """
        dump = xml_dump.Iterator.from_file(codecs.open(file_name, "r", "utf-8"))

        i = 1
        # pages that dont need to be processed
        redirect_page = re.compile('#REDIRECT')
        if (self.dir_out):
            fd = codecs.open("{0}/wiki_processed.txt".
                             format(self.dir_out), 'a', 'utf-8')
        for page in dump:
            fd_log = open('log.txt', "a")
            for revision in page:
                if (not(redirect_page.match(revision.text))):
                    # print("{0} ".format(revision.text.encode('UTF-8')))
                    new_text = process_wiki_str(revision.text)
                    if (self.dir_out):
                        fd = codecs.open("{0}/wiki_processed.txt".
                                         format(self.dir_out), 'a', 'UTF-8')
                        fd.write(new_text)
                        fd.write('\n')
                    print("{0} ".format(page.title.encode('utf-8')))
                    # print(new_text.encode('utf-8'))
                    print()
                fd_log.write(str(page.id) + '\n')
            fd_log.close()
            if (self.dir_out):
                fd.close()
            # if (i==214): break
            i = i+1

    def process2sentences(self, file_name):
        """
        given a text corpus, tokenize to sentences
        tokenizers/punkt/PY3/english.pickle
        """
        fd = codecs.open(file_name, "r", 'UTF-8')

        if (self.dir_out):
            fd_sentences = codecs.open("{0}/wiki_sentences.txt".
                                       format(self.dir_out), 'a', 'UTF-8')
        # how many bytes the method should read
        size_bucket = 27000000
        while(True):
            data = fd.read(size_bucket)
            sent_tokenize_list = sent_tokenize(data)
            print(">> ",len(data))
            if (data == ''):
                break
            if (self.dir_out):
                for sent in sent_tokenize_list:
                    fd_sentences.write("{0}\n".format(sent))

        fd.close()
        if (self.dir_out):
            fd_sentences.close()

    def remove_duplicate_sentences(self, file_name):
        """
         This method remove duplicate sentences from file_name file

         and already tokenize the file

         @string file_name: File name that need to be remove duplicate
              sentences
        """
        fd = codecs.open(file_name, "r", 'UTF-8')
        if (self.dir_out):
            fd_sentences = codecs.open("{0}/wiki_sentences_nodup.txt".
                                       format(self.dir_out), 'a', 'UTF-8')
        old_sentence = fd.readline()
        for sentence in fd:
            if (sentence != old_sentence):
                tokens = word_tokenize(sentence)
                if (len(tokens)>=5 and self.dir_out):
                    token_string = ''
                    for t in tokens: token_string += t + ' '
                    fd_sentences.write("{0}\n".format(token_string))

        fd.close()
        if (self.dir_out):
            fd_sentences.close()
        fd.close()


if __name__ == "__main__":
    dir_out = '/scratch2/evelin.amorim/'
    # dir_out = '/home/disk2/speed/evelin.amorim/Documents/UFMG/wordembedding/'
    pp = PreProcess(dir_out=dir_out)
    # pp = PreProcess()
    train_file = sys.argv[1]

    p_sentences = '-nps'  # nps (not process sentences)
    if (len(sys.argv) >= 3):
        p_sentences = sys.argv[2]
    # ps (process sentences)
    if (p_sentences == '-ps'):
        pp.process2sentences("{0}/wiki_clean.txt".
                             format(dir_out))
        # pp.process2sentences("wikitest.txt")

    dup_sentences = '-nrd'  # nrd (not remove duplicate)
    if (len(sys.argv) >= 4):
        dup_sentences = sys.argv[3]

    # rd (remove duplicate)
    if (dup_sentences == '-rd'):
        pp.remove_duplicate_sentences("{0}/wiki_sorted.txt".
                                      format(dir_out))
