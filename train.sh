#!/bin/bash

onmt_build_vocab -config $1 -n_sample -1
echo "********** Build vocab finished! ************"
echo "********** Training Starting! ************"
nohup onmt_train -config $1 &

# nohup tensorboard --bind_all --logdir='runs/onmt/en-to-hi-aai4b-1' --port=3003 &