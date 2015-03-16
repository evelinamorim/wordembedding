from preprocessing import PreProcess
from config import Config
from train import Train

cfg = Config()

cfg.read('setup.cfg')

pp = PreProcess(cfg.get_option('train_type'))

pp.read_train(cfg.get_option('file_train'))

t = Train(cfg)
model = t.execute(pp.input_train)



