#!/bin/bash

onmt_build_vocab -config config/en-ta.yaml -n_sample -1
echo "********** Build vocab finished! ************"
echo "********** Training Starting! ************"
nohup onmt_train -config config/en-ta.yaml &

# tensorboard --bind_all --logdir='runs/onmt/en-to-hi-aai4b-1' --port=3003