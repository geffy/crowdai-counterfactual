pypy shard_train.py
pypy shard_test.py
cat expected_shard.names | parallel --eta -j2 python3 ./to_pickle.py
cat expected_shard.names | parallel --eta -j1 python3 ./to_sparse.py