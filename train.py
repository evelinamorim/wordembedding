# author: evelin amorim
# description: train wordvec in given data

import os
from gensim.models import word2vec
import config
from nltk.tokenize import word_tokenize


class Train:

    def __init__(self, cfgObj):
        self.__config = cfgObj

    def execute(self, train_input):
        """
           @train  train_input: train input to word2vec
        """

        model_file = self.__config.get_option('model_file')
        model = None
        if (os.path.isfile(model_file)):
            model = word2vec.Word2Vec.load(model_file)
        else:
            fd_input_file = open(train_input, "r")
            sentences = list(map(lambda x: word_tokenize(x.replace('\n', '')),
                                 fd_input_file.readlines()))
            # numero minimo que uma palavra deve aparecer para ser incluida
            # no vocabulario
            min_count_word = int(self.__config.get_option('min_count'))
            # default value
            if (not(min_count_word)):
                min_count_word = 5
            # dimensao do vetor de features
            dim_ftrs = int(self.__config.get_option('dim_ftrs'))
            if (not(dim_ftrs)):
                dim_ftrs = 200
            window_ftrs = int(self.__config.get_option('window_ftrs'))
            if (not(window_ftrs)):
                window_ftrs = 5
            model = word2vec.Word2Vec(window=window_ftrs, size=dim_ftrs,
                                      min_count=min_count_word)
            model.build_vocab(sentences)
            # print(model.vocab)
            model.train(sentences)
            # pickle the entire model to disk, so we can load&resume
            # training later
            model.save(model_file)
            fd_input_file.close()
        return model

if __name__ == '__main__':
    cfgObj = config.Config()
    cfgObj.read('sample.cfg')
    t = Train(cfgObj)
    model = t.execute('/scratch2/evelin.amorim/wiki_sentences_norep.txt')
    # model = t.execute('wiki_sentences_norep_0.txt')
    # print(model.similarity('woman', 'man'))
    # print(model.most_similar(positive=['woman', 'king'], negative=['man'],
    #                         topn=10))
    # print(model.most_similar_cosmul(positive=['woman', 'king'],
    #                                negative=['man'],
    #                                topn=10))
    # print(model.similarity('england', 'ireland'))
    # print(mode.most_similar_cosmul(
    # print(model.most_similar.__doc__)
