import config
import pickle
import sys
import numpy as np
import scipy.sparse as sp
import os

np.random.seed(42)

def convert_sample_to_sparse_faster(sample, is_train=True):
    res = {}
    n_candidates = len(sample['candidates'])
    
    shuffled_idx = list(range(n_candidates))
    if is_train:
        np.random.shuffle(shuffled_idx)
    
    sp_i, sp_j, sp_d = [], [], []
    for i, idx in enumerate(shuffled_idx):
        candidate = sample['candidates'][idx]
        sp_i.extend([i]*len(candidate))
        sp_j.extend(candidate.keys())
        sp_d.extend(candidate.values())
        if idx == 0 and is_train:
            res = {
                'observed_idx': i,
                'click': (sample['cost'] < 0.5)*1,
                'cost': sample['cost'],
                'propensity': sample['propensity']
    }
    res['id'] = sample['id']
    res['mat'] = sp.coo_matrix((sp_d, (sp_i, sp_j)), shape=(n_candidates, 74000), dtype=np.int16)
    res['n_candidates'] = n_candidates
    return res

def batched_converter(batch):
    return [convert_sample_to_sparse_faster(x, is_train=arg.startswith('train')) for x in batch]

arg = sys.argv[1].strip().lower()
os.makedirs(config.SPARSE_DIR, exist_ok=True)

from multiprocessing import Pool
from more_itertools import chunked
import itertools
p = Pool(5)

ds = pickle.load(open(config.PICKLED_DIR + '/{}.pickled'.format(arg), 'rb'))
list2d = p.map(batched_converter, chunked(ds, 100000))
converted_ds = list(itertools.chain.from_iterable(list2d))
pickle.dump(converted_ds, file=open(config.SPARSE_DIR + '/{}.pickled'.format(arg), 'wb'), protocol=-1)