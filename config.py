

class Config:

    def __init__(self):
	self.__options = {}

    def read(self,file_name):

	fd = open(file_name,"r")

	for line in file_name:
	    option_list = line.split('=')
	    if (len(option_list)<2):
		print "Warning ** ",line," ** does not have correct options"
	    else:
		option_name = option_list[0]
		option_value = option_list[1].replace('\n','')
		self.__options[option_name] = option_value
	fd.close()

    def get_option(self,option_name):
	return self.__options[option_name]

    def set_option(self,option_name,option_value):
	self.__options[option_name] = option_value
