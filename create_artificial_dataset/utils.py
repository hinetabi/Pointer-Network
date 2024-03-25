import re


def tokenize(sentence):
    """Tokenize the sentence by space and punctuation

    Args:
        sentence (str): input sentence

    Returns:
        List[str]: list of tokenized string.
    """
    def is_word_ended_with_punctuation(word):
      # Define the set of punctuation marks
      punctuation_marks = "[.,;:'\"()?!-#]+"
      # Create a regular expression pattern to match the word ending with punctuation
      pattern = re.compile(fr"{punctuation_marks}$")
      # Check if the word matches the pattern
      if pattern.search(word):
          return True
      else:
          return False

    def is_word_start_with_punctuation(word):
      # Define the set of punctuation marks
      punctuation_marks = "[.,;:'\"()?!-#]+"
      # Create a regular expression pattern to match the word ending with punctuation
      pattern = re.compile(fr"^{punctuation_marks}")
      # Check if the word matches the pattern
      if pattern.search(word):
          return True
      else:
          return False

    # Tokenize based on spaces
    words = sentence.split()
    # Process each word to split punctuation in the last words
    tokenized_words = []
    for word in words:
        # Use regular expression to separate punctuation from the word
        part1 = ""
        part2 = ""

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

    return tokenized_words

def append_sent_to_file(file_path, dataset):
    with open(file_path, 'a',encoding = 'utf-8') as file:
        for line in dataset:
            file.write(line+'\n')