import config

print('Start to shard test () file from {} to {} dir'.format(config.RAW_TEST, config.SHARDS_DIR))

fin = open(config.RAW_TEST)
buf = []

# approximately 1/8 of test set
nBuf = 12000000

# counter of output shards
nOut = 0

print('Open {} shard'.format(nOut))
fOut = open(config.SHARDS_DIR + "/test_{}".format(nOut), 'w')
for line in fin:
    buf.append(line)
    if len(buf) > nBuf:
        if buf[-1].split()[0] != buf[-2].split()[0]:
            fOut.write(''.join(buf[:-1]))
            fOut.close()
            nOut += 1
            print('Open {} shard'.format(nOut))
            fOut = open(config.SHARDS_DIR + "/test_{}".format(nOut), 'w')
            buf = []
            buf.append(line)
fOut.write(''.join(buf))
fOut.close()
print("Done!")