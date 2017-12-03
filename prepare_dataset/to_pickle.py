import json
import pickle
import sys
from criteo_dataset import CriteoDataset
import config
import os

arg = sys.argv[1].strip().lower()
os.makedirs(config.PICKLED_DIR, exist_ok=True)
ds = [x for x in CriteoDataset(config.SHARDS_DIR + "/{}".format(arg), isTest=arg.startswith('test_'))]
pickle.dump(ds, file=open(config.PICKLED_DIR + '/{}.pickled'.format(arg), 'wb'), protocol=-1)