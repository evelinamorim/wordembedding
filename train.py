#author: evelin amorim
#description: train wordvec in given data

import os
from gensim.models import word2vec

class Train:

    def __init__(self,cfgObj):
	self.__config = cfgObj


    def execute(self,train_input):
	"""
	@train  train_input: train input to word2vec
	"""
	model_file = self.__config['model_file']
	model = None
        if (os.path.isfile(model_file)):
	    #dimensao do vetor de features
	    dim_ftrs=200
	    if ('dim_ftrs' in self.__config):
	        dim_ftrs = self.__config['dim_ftrs']
	    window=5
	    if ('window_ftrs' in self.__config):
	        window_ftrs = self.__config['window_ftrs']

	    model = word2vec.Word2Vec(train_input, window=window_ftr,size=dim_ftrs)
	    # pickle the entire model to disk, so we can load&resume training later
	    model.save(model_file)
	else:
	    model = word2vec.Word2Vec.load(model_file)
	return model
