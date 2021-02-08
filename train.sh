#!/bin/bash

onmt_build_vocab -config config/en-bn.yaml -n_sample -1
echo "********** Build vocab finished! ************"
echo "********** Training Starting! ************"
nohup onmt_train -config config/en-bn.yaml &

# nohup tensorboard --bind_all --logdir='runs/onmt/en-to-hi-aai4b-1' --port=3003 &