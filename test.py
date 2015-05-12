import sys
import gensim
import time


class ReadCorpus:
    """
    Read corpus for some tasks. Nowadays, there is only two corpus:
        * MSR: research.microsoft.com/en-us/
        projects/rnn/
        * Google: code.google.com/p/word2vec/source/
        browse/trunk/questions-words.txt
    """

    def __init__(self, corpus_type):
        """
        Read some corpus

        @corpus_type string: which type this object will process
        """
        self.__corpus_type = corpus_type

    def read(self, input_file):
        """
        Read and store in memory the corpus file.

        Each analogy is a tuple and it returns a list with tuples

        @input_file string: input_file with the analogy questions
        """
        if (self.__corpus_type == 'analogy'):
            return self.read_analogy(input_file)
        else:
            print("** Warning ** Corpus not read. ", self.__corpus_type,
                  'is not valid')

    def read_analogy(self, input_file):
        """
        Read and store in memory the corpus file.

        Each analogy is a tuple and it returns a lista with tuples

        @input_file string: input_file with the analogy questions
        """
        fd = open(input_file, 'r')
        corpus_lst = []
        for line in fd:
            word_list = line.split()
            if (len(word_list) >= 3):
                corpus_lst.append((word_list[0], word_list[1], word_list[2]))

        fd.close()
        return corpus_lst


class Test:

    """
    Perform test according to a given vector word file
    """

    def __init__(self, task_type, dir_out='out'):
        """
        @string task_type: The type of the task that the testing needs to
        perform
        """

        self.__task_type = task_type
        self.__dir_out = dir_out

    def execute(self, vector_file, task_file):
        """

        @string vector_file: The name of the binary file with word vectors

        Read a task file, and then return the answers according to
        the vector file given. It returns the answer to perform perfomance
        tasks
        """
        rc = ReadCorpus(self.__task_type)
        corpus = rc.read(task_file)
        model = gensim.models.Word2Vec.load_word2vec_format(vector_file,
                                                            binary=True)
        answer = self.execute_task(model, corpus)

        return answer

    def execute_task(self, model, corpus):
        """
        @model object: The model object of vector words
        @list: A list with elements from a corpus

        Execute the task given in the class instatiation
        """

        if (self.__task_type == 'analogy'):
            return self.execute_analogy(model, corpus)

    def execute_analogy(self, model, corpus):
        t = time.gmtime()
        self.__result_file = "{0}/results{1}{2}{3}_{4}{5}{6}.txt".format(
                                                              self.__dir_out,
                                                              t.tm_year,
                                                              t.tm_mon,
                                                              t.tm_mday,
                                                              t.tm_hour,
                                                              t.tm_min,
                                                              t.tm_sec)
        fd = open(self.__result_file, "w")
        i = 0
        for el in corpus:
            a = el[0].lower()
            a_star = el[1].lower()
            b = el[2].lower()
            # TODO: nao sei se pega soh o primeiro mesmo
            try:
                top = model.most_similar(positive=[a_star, b],
                                                negative=[a])[0]
                fd.write("{0} {1}\n".format(i, top))
            except KeyError:
                print("Error: ", a_star, b, a)
            i = i + 1
        fd.close()

if __name__ == '__main__':
    vector_file = sys.argv[1]
    task_file = sys.argv[2]
    tobj = Test('analogy')
    tobj.execute(vector_file, task_file)
