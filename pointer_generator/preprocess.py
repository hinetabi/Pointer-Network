#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from itertools import zip_longest
import re


def replace_oovs(source_in, target_in, vocabulary, source_out, target_out):
    """Replaces out-of-vocabulary words in source and target text with <unk-N>,
    where N in is the position of the word in the source sequence.
    """

    def format_unk(pos):
        return "<unk-{}>".format(pos)

    if target_in is None:
        target_in = []

    for seq_num, (source_seq, target_seq) in enumerate(
        zip_longest(source_in, target_in)
    ):
        source_seq_out = []
        target_seq_out = []

        word_to_pos = dict()
        for position, token in enumerate(source_seq.strip().split()):
            if token in vocabulary:
                token_out = token
            else:
                if token in word_to_pos:
                    oov_pos = word_to_pos[token]
                else:
                    word_to_pos[token] = position
                    oov_pos = position
                token_out = format_unk(oov_pos)
            source_seq_out.append(token_out)
        source_out.write(" ".join(source_seq_out) + "\n")

        if target_seq is not None:
            for token in target_seq.strip().split():
                if token in word_to_pos:
                    token_out = format_unk(word_to_pos[token])
                else:
                    token_out = token
                target_seq_out.append(token_out)
        if target_out is not None:
            target_out.write(" ".join(target_seq_out) + "\n")

def add_oov_sentence(sentence, vocab_file):
    """Replaces out-of-vocabulary words in source and target text with <unk-N>,
    where N in is the position of the word in the source sequence.
    """

    def format_unk(pos):
        return "<unk-{}>".format(pos)
    
    with open(vocab_file, encoding="utf-8") as vocab:
        vocabulary = [line.split(" ")[0] for line in vocab.read().splitlines()]

    word_to_pos = dict()
    source_seq_out = []
    for position, token in enumerate(sentence.strip().split()):
        if token in vocabulary:
            token_out = token
        else:
            if token in word_to_pos:
                oov_pos = word_to_pos[token]
            else:
                word_to_pos[token] = position
                oov_pos = position
            token_out = format_unk(oov_pos)
        source_seq_out.append(token_out)
                
    return " ".join(source_seq_out) + "\n"

def reformat_sentence(sentence):
    """Tokenize the sentence by space and punctuation

    Args:
        sentence (str): input sentence

    Returns:
        List[str]: list of tokenized string.
    """
    def is_word_ended_with_punctuation(word):
      # Define the set of punctuation marks
      punctuation_marks = "[.,;:'\"()?!-]+"
      # Create a regular expression pattern to match the word ending with punctuation
      pattern = re.compile(fr"{punctuation_marks}$")
      # Check if the word matches the pattern
      if pattern.search(word):
          return True
      else:
          return False

    def is_word_start_with_punctuation(word):
      # Define the set of punctuation marks
      punctuation_marks = "[.,;:'\"()?!-]+"
      # Create a regular expression pattern to match the word ending with punctuation
      pattern = re.compile(fr"^{punctuation_marks}")
      # Check if the word matches the pattern
      if pattern.search(word):
          return True
      else:
          return False

    # Tokenize based on spaces
    words = sentence.strip().split(" ")
    # Process each word to split punctuation in the last words
    tokenized_words = []
    for word in words:
        # Use regular expression to separate punctuation from the word
        part1 = ""
        part2 = ""
        if word == "":
          tokenized_words.append(word)
          continue
        while is_word_ended_with_punctuation(word):
          part2 = word[-1] + part2
          word = word[:-1]

        while is_word_start_with_punctuation(word):
          part1 = part1 + word[0]
          word = word[1:]

        if part1 != "":
          tokenized_words.append(part1)
        if word != "":
          tokenized_words.append(word)
        if part2 != "":
          tokenized_words.append(part2)

    return " ".join(tokenized_words)
    
def main():
    parser = argparse.ArgumentParser(
        description="Replaces out-of-vocabulary words in both source and target "
        "sequences with tokens that indicate the position of the word "
        "in the source sequence."
    )
    parser.add_argument(
        "--source", type=str, help="text file with source sequences", required=True
    )
    parser.add_argument(
        "--target", type=str, help="text file with target sequences", default=None
    )
    parser.add_argument("--vocab", type=str, help="vocabulary file", required=True)
    parser.add_argument(
        "--source-out",
        type=str,
        help="where to write source sequences with <unk-N> entries",
        required=True,
    )
    parser.add_argument(
        "--target-out",
        type=str,
        help="where to write target sequences with <unk-N> entries",
        default=None,
    )
    args = parser.parse_args()

    with open(args.vocab, encoding="utf-8") as vocab:
        vocabulary = vocab.read().splitlines()

    target_in = (
        open(args.target, "r", encoding="utf-8") if args.target is not None else None
    )
    target_out = (
        open(args.target_out, "w", encoding="utf-8")
        if args.target_out is not None
        else None
    )
    with open(args.source, "r", encoding="utf-8") as source_in, open(
        args.source_out, "w", encoding="utf-8"
    ) as source_out:
        replace_oovs(source_in, target_in, vocabulary, source_out, target_out)
    if target_in is not None:
        target_in.close()
    if target_out is not None:
        target_out.close()


if __name__ == "__main__":
    main()
