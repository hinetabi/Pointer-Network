## Training the pointer-generator model on our dataset

##### 1. Download the our data and preprocess it

Download the data from [here](https://github.com/EdinburghNLP/XSum) to obtain our dataset. You should have four files,
{train,validation}.{src,tgt}.

The testing dataset is avalable [here](https://github.com/VSEC2021/VSEC).

The weights of our best model is available [here](https://drive.google.com/file/d/1loXhJqKoAC902m7TtkZJoggA0d4uCFZs/view?usp=drive_link).

##### 2. Create a vocabulary and extend it with source position markers

```bash
vocab_size=10000
position_markers=200
export LC_ALL=C
cat train.src train.tgt \
  tr -s '[:space:]' '\n' \
  sort \
  uniq -c \
  sort -k1,1bnr -k2 \
  head -n "$((vocab_size - 4))" \
  awk '{ print $2 " " $1 }' >dict.pg.txt
python3 -c "[print('<unk-{}> 0'.format(n)) for n in range($position_markers)]" >>dict.pg.txt
```

This creates the file dict.pg.txt that contains the 10k most frequent words, followed by 200 source position markers:

```
the 4954867
. 4157552
, 3439668
to 2212159
a 1916857
of 1916820
and 1823350
...
<unk-0> 0
<unk-1> 0
<unk-2> 0
<unk-3> 0
<unk-4> 0
...
<unk-199> 0
```

##### 2. Preprocess the text data

```bash
$ python pointer_generator/preprocess.py --source train.src --target train.tgt --vocab <(cut -d' ' -f1 dict.pg.txt) --source-out train.pg.src --target-out train.pg.tgt

$ python pointer_generator/preprocess.py --source validation.src --target validation.tgt --vocab <(cut -d' ' -f1 dict.pg.txt) --source-out valid.pg.src --target-out valid.pg.tgt

$ python pointer_generator/preprocess.py --source test.src --vocab <(cut -d' ' -f1 dict.pg.txt) --source-out test.pg.src
```

The data should now contain `<unk-N>` tokens in place of out-of-vocabulary words.

##### 3. Binarize the dataset:

```bash
fairseq-preprocess \
  --source-lang src \
  --target-lang tgt \
  --trainpref train.pg \
  --validpref valid.pg \
  --destdir bin \
  --workers 60 \
  --srcdict dict.pg.txt \
  --joined-dictionary
```

##### 3. Train a model

```bash
total_updates=20000
warmup_updates=500
lr=0.001
max_tokens=4096
update_freq=4
pointer_layer=-2

CUDA_VISIBLE_DEVICES=0 fairseq-train bin \
    --user-dir pointer_generator/pointer_generator_src \
    --max-tokens "$max_tokens" \
    --task translation \
    --source-lang src --target-lang tgt \
    --truncate-source \
    --layernorm-embedding \
    --share-all-embeddings \
    --encoder-normalize-before \
    --decoder-normalize-before \
    --required-batch-size-multiple 1 \
    --arch transformer_pointer_generator \
    --alignment-layer "$pointer_layer" \
    --alignment-heads 1 \
    --source-position-markers 200 \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing 0.1 \
    --dropout 0.1 --attention-dropout 0.1 \
    --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.999)" --adam-eps 1e-08 \
    --clip-norm 0.1 \
    --lr-scheduler inverse_sqrt --lr "$lr" --max-update "$total_updates" --warmup-updates "$warmup_updates" \
    --update-freq "$update_freq" \
    --skip-invalid-size-inputs-valid-test
```

Above we specify that our dictionary contains 200 source position markers, and
that we want to use one attention head from the penultimate decoder layer for
pointing. 

##### 4. Correct the test sequences

```bash
batch_size=32
beam_size=6
max_length=60
length_penalty=1.0

fairseq-interactive bin \
    --user-dir pointer_generator/pointer_generator_src \
    --batch-size "$batch_size" \
    --task translation \
    --source-lang src --target-lang tgt \
    --path checkpoints/checkpoint_last.pt \
    --input test.pg.src \
    --buffer-size 200 \
    --max-len-a 0 \
    --max-len-b "$max_length" \
    --lenpen "$length_penalty" \
    --beam "$beam_size" \
    --skip-invalid-size-inputs-valid-test |
    tee generate.out
grep ^H generate.out | cut -f 3- >generate.hyp
```

Now you should have the generated sequences in `generate.hyp`. They contain
`<unk-N>` tokens that the model has copied from the source sequence. In order to
retrieve the original words, we need the unprocessed source sequences from
`test.src`.

##### 5. Process the generated output

Since we skipped too long inputs when producing `generate.hyp`, we also have to
skip too long sequences now that we read `test.src`.

```bash
./postprocess.py \
    --source <(awk 'NF<1024' test.src) \
    --target generate.hyp \
    --target-out generate.hyp.processed
```

Now you'll find the final sequences from `generate.hyp.processed`, with
`<unk-N>` replaced with the original word from the source sequence.

##### An example of a summarized sequence

The original source src in `test.src`:

> de roon moved to teesside in june 2016 for an initial # 8.8 m fee and played 33 premier league games last term . the netherlands international , 26 , scored five goals in 36 league and cup games during his spell at boro . meanwhile , manager garry monk confirmed the championship club 's interest in signing chelsea midfielder lewis baker . `` he 's a target and one of many that we 've had throughout the summer months , '' said monk . find all the latest football transfers on our dedicated page .

The preprocessed source src in `test.src.pg`:

> de \<unk-1> moved to \<unk-4> in june 2016 for an initial # \<unk-12> m fee and played 33 premier league games last term . the netherlands international , 26 , scored five goals in 36 league and cup games during his spell at boro . meanwhile , manager garry monk confirmed the championship club 's interest in signing chelsea midfielder lewis baker . `` he 's a target and one of many that we 've had throughout the summer months , '' said monk . find all the latest football transfers on our dedicated page .

The generated tgt in `generate.hyp`:

> middlesbrough striker \<unk> de \<unk-1> has joined spanish side \<unk> on a season-long loan .

The generated tgt after postprocessing in `generate.hyp.processed`:

> middlesbrough striker \<unk> de roon has joined spanish side \<unk> on a season-long loan .
