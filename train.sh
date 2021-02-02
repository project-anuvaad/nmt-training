onmt_build_vocab -config config/test.yaml -n_sample -1

onmt_train -config config/test.yaml

tensorboard --logdir='runs/onmt/' --port=3003