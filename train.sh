#!/bin/bash

onmt_build_vocab -config config/en-bn.yaml -n_sample -1
echo "********** Build vocab finished! ************"
echo "********** Training Starting! ************"
onmt_train -config config/en-bn.yaml

# tensorboard --logdir='runs/onmt/' --port=3003