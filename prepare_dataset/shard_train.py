import config
import os
print('Start to shard train file from {} to {}/train_{}'.format(config.RAW_TRAIN, config.SHARDS_DIR, '{shardId}'))

fin = open(config.RAW_TRAIN)
n_shards = 16

try:
    os.makedirs(config.SHARDS_DIR)
except:
    print('cannot create SHARDS_DIR directory, maybe already exists?')
fouts = [open(config.SHARDS_DIR + '/train_{}'.format(i), 'w') for i in range(n_shards)]

n_lines = 0
for line in fin:
    curr_id = int(line.split('|')[0].strip())   
    fouts[curr_id%n_shards].write(line)
    n_lines += 1
    if n_lines % 1000000 == 0:
        print('\t {}M lines processed'.format(n_lines / 1000000))
        
[f.close() for f in fouts]
print("Done!")