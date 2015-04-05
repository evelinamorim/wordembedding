# sort by mul-tithreading a file with lines
import threading
import queue

# help:
# (i) mudar o tamanho da linha para colocar ou retirar a quantidade
# de dados da memoria.
# (ii) verificar o numero de nucleos do processador para saber
# o numero que devo colocar em max_threads


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.sort_data = []

    def run(self):
        sp = SortParallel()
        data = self.q.get()
        print("**** Thread {0} running ****".format(self.threadID))
        # fd = open("{0}.txt".format(self.threadID), "w")
        # for line in data:
        #    fd.write("{0}\n".format(line))
        # fd.close()
        sp.mergesort(data, 0, len(data)-1)
        self.sort_data = data


class SortParallel:

    def __init__(self, size_bucket=10000):
        # how many lines the bucket must have
        self.__size_bucket = size_bucket
        # suposto tamanho de uma linha: 120 bytes. Aqui eu aumento
        # a quantidade de dados que vai na memoria
        self.__len_line = 180
        self.__max_threads = 3

    def merge(self, data, b, m, e):
        """
        merge a data list
        b:  begin
        m: middle
        e: end
        """
        n1 = m - b + 1
        n2 = e - m
        left = data[b:(b+n1)]
        len_left = len(left)
        right = data[m+1:(m+n2+1)]
        len_right = len(right)

        i = j = 0
        nequals = 0
        for k in range(b, e+1):
            if (j >= len_right and i < len_left):
                data[k] = left[i]
                i = i+1
            elif (i >= len_left and j < len_right):
                data[k] = right[j]
                j = j+1
            else:
                if (i < len_left and j < len_right):
                    if (left[i] < right[j]):
                        data[k] = left[i]
                        i = i+1
                    else:
                        if (left[i] == right[j]):
                            i = i + 1
                            nequals = nequals + 1
                        data[k] = right[j]
                        j = j+1

        while (nequals != 0):
            end = len(data)-1
            data.pop(end)
            nequals = nequals - 1

    def mergesort(self, data, b, e):
        """
        sort by mergesort data
        parallel!!!
        """

        if (b < e):
            m = (b+e) // 2
            self.mergesort(data, b, m)
            self.mergesort(data, m+1, e)
            self.merge(data, b, m, e)

    def split_bucket(self, i, file_name):
        """
        Given the file_name, this function returns
        the data to sort
        """
        pos = (self.__len_line*self.__size_bucket)*i

        fd = open(file_name, "r")
        fd.seek(pos)
        data = fd.read(self.__len_line*self.__size_bucket)

        len_data = len(data)
        if (len_data > 0):
            byte_ini = fd.read(1)
            # print("++", len_data)
            if (data[len_data-1] != '\n'):
                # acertando o fim
                byte = byte_ini
                while (byte and byte != '\n'):
                    data += byte
                    byte = fd.read(1)

            # acertar o inicio
            if (i != 0 and byte_ini != '\n'):
                # testando se estou no inicio de uma linha
                byte = byte_ini
                i = 0
                while (byte and byte != '\n'):
                    i = i + 1
                    byte = fd.read(1)
                data = data[i:]
            fd.close()
            return data.split('\n')
        else:
            return []

    def parallel_sort(self, round_exec, file_name):
        """
        Given a file, perform a parallel sorting, using mergesort

        This will be to act like a "master" of threads
        """
        q = queue.Queue(self.__max_threads)
        nbuckets = 3
        i = round_exec*nbuckets
        end_bucket = nbuckets + i
        # print("-->", i)
        thread_list = []
        queueLock = threading.Lock()

        while (i < end_bucket):
            id_list = []

            queueLock.acquire()
            for k in range(0, self.__max_threads):
                q.put(self.split_bucket(i, file_name))
                id_list.append(i)
                if (i >= end_bucket):
                    break
                i = i + 1
            queueLock.release()
            # print(id_list, self.__max_threads)
            nthreads = len(id_list)
            for k in range(nthreads):
                thread = myThread(id_list.pop(), "sort", q)
                thread.start()
                thread_list.append(thread)

            while not q.empty():
                pass

        result = []
        for t in thread_list:
            t.join()
            middle = len(result)
            print(">> ", len(t.sort_data))
            result += t.sort_data
            end = len(result) - 1
            self.merge(result, 0, middle, end)

        fd = open("wiki_sentences_norep_{0}.txt".format(round_exec), "w")
        for d in result:
            fd.write("{0}\n".format(d))
        fd.close()

if __name__ == '__main__':
    sp = SortParallel()
    for x in range(4):
        sp.parallel_sort(x, '../data/sample_sentences.txt')
