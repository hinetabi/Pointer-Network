# -*- coding: utf-8 -*-

# This code is from https://github.com/abisee/cnn-dailymail.git

import sys
import os
import hashlib
import struct
import subprocess
import collections
from tensorflow.core.example import example_pb2

dm_single_close_quote = u'\u2019'  # unicode
dm_double_close_quote = u'\u201d'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote,
              ")"]  # acceptable ways to end a sentence

# We use these to separate the summary sentences in the .bin datafiles
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'

tokenized_dir = ""
finished_files_dir = ""
chunks_dir = ""

# These are the number of .story files we expect there to be in cnn_stories_dir and dm_stories_dir
num_expected_cnn_stories = 92579
num_expected_dm_stories = 219506

VOCAB_SIZE = 200000
CHUNK_SIZE = 1000  # num examples per chunk, for the chunked data


def chunk_file(set_name):
    in_file = 'dataset/finished_files/%s.bin' % set_name
    reader = open(in_file, "rb")
    chunk = 0
    finished = False
    while not finished:
        chunk_fname = os.path.join(chunks_dir, '%s_%03d.bin' % (set_name, chunk))  # new chunk
        with open(chunk_fname, 'wb') as writer:
            for _ in range(CHUNK_SIZE):
                len_bytes = reader.read(8)
                if not len_bytes:
                    finished = True
                    break
                str_len = struct.unpack('q', len_bytes)[0]
                example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
                writer.write(struct.pack('q', str_len))
                writer.write(struct.pack('%ds' % str_len, example_str))
            chunk += 1


def chunk_all():
    # Make a dir to hold the chunks
    if not os.path.isdir(chunks_dir):
        os.mkdir(chunks_dir)
    # Chunk the data
    for set_name in ['train', 'val', 'test']:
        print("Splitting %s data into chunks..." % set_name)
        chunk_file(set_name)
    print("Saved chunked data in %s" % chunks_dir)

def read_text_file(text_file):
    lines = []
    with open(text_file, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines

def write_to_bin(train_test_val, out_file, makevocab=False):
    """Reads the tokenized .story files corresponding to the urls listed in the url_file and writes them to a out_file."""
    print("Making bin file for %s..." % train_test_val)
    # url_list = read_text_file(url_file)
    # url_hashes = get_url_hashes(url_list)
    fnames = [f'{train_test_val}_{des}.txt' for des in ['src', 'tgt']]
    num_stories = len(fnames)

    if makevocab:
        vocab_counter = collections.Counter()

    with open(out_file, 'wb') as writer:
        # Look in the tokenized story dirs to find the .story file corresponding to this url
        if os.path.isfile(os.path.join(tokenized_dir, fnames[0])) and os.path.isfile(os.path.join(tokenized_dir, fnames[1])):
            src_file = os.path.join(tokenized_dir, fnames[0])
            tgt_file = os.path.join(tokenized_dir, fnames[1])
        else:
            raise Exception(f"File {fnames[0]} and {fnames[1]} is not available in directory {tokenized_dir}")
        # Get the strings to write to .bin file
        with open(src_file, 'r') as f:
            src = f.readlines()
        with open(tgt_file, 'r') as f:
            tgt = f.readlines()
            
        for article, abstract in zip(src, tgt):
            abstract = f"{SENTENCE_START} {abstract} {SENTENCE_END}"
            # Write to tf.Example
            tf_example = example_pb2.Example()
            tf_example.features.feature['article'].bytes_list.value.extend([bytes(article, encoding='utf-8')])
            tf_example.features.feature['abstract'].bytes_list.value.extend([bytes(abstract, encoding='utf-8')])
            tf_example_str = tf_example.SerializeToString()
            str_len = len(tf_example_str)
            writer.write(struct.pack('q', str_len))
            writer.write(struct.pack('%ds' % str_len, tf_example_str))

            # Write the vocab to file, if applicable
            if makevocab:
                art_tokens = article.split(' ')
                abs_tokens = abstract.split(' ')
                abs_tokens = [t for t in abs_tokens if
                                t not in [SENTENCE_START, SENTENCE_END]]  # remove these tags from vocab
                tokens = art_tokens + abs_tokens
                tokens = [t.strip() for t in tokens]  # strip
                tokens = [t for t in tokens if t != ""]  # remove empty
                vocab_counter.update(tokens)

    print("Finished writing file %s\n" % out_file)

    # write vocab to file
    if makevocab:
        print( "Writing vocab file...")
        with open(os.path.join(finished_files_dir, "vocab"), 'w') as writer:
            for word, count in vocab_counter.most_common(VOCAB_SIZE):
                writer.write(word + ' ' + str(count) + '\n')
        print("Finished writing vocab file")

if __name__ == '__main__':
    """Usage example: python make_datafiles.py dataset/train_500k_new_error dataset/finished_files
    """
    if len(sys.argv) != 3:
        print("USAGE: python make_datafiles.py <tokenized_dir> <finished_files_dir>")
        sys.exit()
        
    tokenized_dir = sys.argv[1]
    finished_files_dir = sys.argv[2]
    chunks_dir = os.path.join(finished_files_dir, "chunked")

    # Create some new directories
    if not os.path.exists(tokenized_dir): os.makedirs(tokenized_dir)
    if not os.path.exists(finished_files_dir): os.makedirs(finished_files_dir)

    # tokenize_stories(cnn_stories_dir, cnn_tokenized_stories_dir)
    # tokenize_stories(dm_stories_dir, dm_tokenized_stories_dir)

    # Read the tokenized stories, do a little postprocessing then write to bin files
    write_to_bin('test', os.path.join(finished_files_dir, "test.bin"))
    write_to_bin('val', os.path.join(finished_files_dir, "val.bin"))
    write_to_bin('train', os.path.join(finished_files_dir, "train.bin"), makevocab=True)

    # Chunk the data. This splits each of train.bin, val.bin and test.bin into smaller chunks, each containing e.g. 1000 examples, and saves them in finished_files/chunks
    chunk_all()
