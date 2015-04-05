# sort by mul-tithreading a file with lines
import threading
import queue


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        sp = SortParallel()
        data = self.q.get()
        print("**** Thread {0} running ****".format(self.threadID))
        sp.mergesort(data, 0, len(data)-1)
        # fd = open("{0}.txt".format(self.threadID), "w")
        # for line in data:
        #    fd.write("{0}\n".format(line))
        # fd.close()


class SortParallel:

    def __init__(self, size_bucket=10000):
        self.__nlines = 99999
        # how many lines the bucket must have
        self.__size_bucket = size_bucket
        # suposto tamanho de uma linha: 120 bytes
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
        byte_ini = fd.read(1)
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

    def parallel_sort(self, file_name):
        """
        Given a file, perform a parallel sorting, using mergesort

        This will be acting like a "master" of threads
        """
        q = queue.Queue(self.__max_threads)
        i = 0
        # nbuckets = self.__nlines/self.__size_bucket
        nbuckets = 3
        thread_list = []
        queueLock = threading.Lock()

        while (i < nbuckets):
            id_list = []

            queueLock.acquire()
            for k in range(0, self.__max_threads):
                q.put(self.split_bucket(i, file_name))
                id_list.append(i)
                if (i >= nbuckets):
                    break
                i = i + 1
            queueLock.release()
            # print(id_list, self.__max_threads)
            for k in range(self.__max_threads):
                thread = myThread(id_list.pop(), "sort", q)
                thread.start()
                thread_list.append(thread)

            while not q.empty():
                pass

        for t in thread_list:
            t.join()


if __name__ == '__main__':
    sp = SortParallel()
    sp.parallel_sort('../data/sample_sentences.txt')
