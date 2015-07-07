

class Config:

    def __init__(self):
        self.__fields = {}

    def read(self, fileName):
        fd = open(fileName, 'r')
        for line in fd:
            lst = line.replace('\n', '').split('=')
            conf_values = lst[1].split(';')
            for v in conf_values:
                lst_v = v.split(',')
                if len(lst_v) > 1:
                    self.__fields[lst[0]] = lst_v
                else:
                    self.__fields[lst[0]] = v
        fd.close()

    def get_field(self, fieldName):
        if fieldName in self.__fields:
            return self.__fields[fieldName]
        else:
            return None
