This repository contain code for 2nd place winning solution of [Criteo Ad Placement Challenge](https://www.crowdai.org/challenges/nips-17-workshop-criteo-ad-placement-challenge) hosted by [crowdAI](https://www.crowdai.org).

## How to build the solution
1. `cd prepare_dataset`
2. Set paths in `config.py` (warning: around 130 GB of free disk space is needed)
3. Run `build.sh` (this takes about 2h on my setup)
4. After dataset processing, go back, `cd ..`
5. Start jupyter notebook
6. Open and execute every cell in `make_batches.ipynb`
7. Open and execute every cell in `learn_model.ipynb` (in parallel with learning you can start tensorboard to see progress)
8. File `{TMP_DIR}/submit_scaled.gz` will produce `IPS: 54.556` on the leaderboard.

Some details about the approach you can find in `docs` folder.

## Dependencies
* pypy (5.1.2)
* python (3.5.2)
* notebook (5.2.1)
* numpy (1.13.3)
* scipy (1.0.0)
* tensorflow-gpu (1.4.0)
* tensorflow-tensorboard (0.4.0rc2)
* tqdm (4.19.4)

## Hardware requirements
This code was executed on machine with 64G RAM, i7-6800K core and NVIDIA GTX 1080 running under Linux Mint 18.1 (not tested, but should run without GPU and with less RAM).

## Promotion
If you want to learn useful ML techniques and competition specific tricks, check out [this course](https://www.coursera.org/learn/competitive-data-science/home/welcome) from experienced kagglers like me and KazAnova.
