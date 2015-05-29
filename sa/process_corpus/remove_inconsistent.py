# remove inconsistent registers
import sys
import json

data_file = sys.argv[1]

fd = open(data_file, 'r')
fd_new = open('novo_%s' % data_file, 'w')

i = 0
for line in fd:
    reg = json.loads(line)
    if 'easeOfUse' in reg:
        if 'satisfaction' in reg:
            if 'effectiveness' in reg:
                if (reg['easeOfUse'] <= 5 and reg['satisfaction'] <= 5 and
                    reg['effectiveness'] <= 5):
                        fd_new.write(line)
                else:
                    print(i, ': easeOfUse ', reg['easeOfUse'])
                    print(i, ': satisfaction ', reg['satisfaction'])
                    print(i, ': effectiveness ', reg['effectiveness'])
    i = i + 1

fd.close()
fd_new.close()
