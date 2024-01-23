# -*- coding: utf-8 -*-

import os

SENTENCE_STA = '<s>'
SENTENCE_END = '</s>'

UNK = 0
PAD = 1
BOS = 2
EOS = 3

PAD_TOKEN = '[PAD]'
UNK_TOKEN = '[UNK]'
BOS_TOKEN = '[BOS]'
EOS_TOKEN = '[EOS]'

beam_size=4
emb_dim= 512
batch_size= 1
batch_queue_max= 500000 // batch_size + 1
hidden_dim= 1024
max_enc_steps=400
max_dec_steps=100
max_tes_steps=100
min_dec_steps=35
vocab_size=10000

lr=0.05
cov_loss_wt = 1.0
pointer_gen = True
is_coverage = False

max_grad_norm=2.0
adagrad_init_acc=0.1
rand_unif_init_mag=0.02
trunc_norm_init_std=1e-4

eps = 1e-12
use_gpu=True
lr_coverage=0.15
max_iterations=50000

# transformer
d_k = 64
d_v = 64
n_head = 6
tran = False
dropout = 0.1
n_layers = 3
d_model = 128
d_inner = 512
n_warmup_steps = 4000

root_dir = os.path.expanduser("./")
log_root = os.path.join(root_dir, "dataset/log/")
# save models when complete 500 iters
save_model_every = 7800

#train_data_path = os.path.join(root_dir, "pointer_generator/dataset/finished_files/train.bin")
train_data_path = os.path.join(root_dir, "dataset/finished_files/chunked/train_*")
eval_data_path = os.path.join(root_dir, "dataset/finished_files/val.bin")
decode_data_path = os.path.join(root_dir, "dataset/finished_files/test.bin")
vocab_path = os.path.join(root_dir, "dataset/finished_files/vocab")
