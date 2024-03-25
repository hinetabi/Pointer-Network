# How to create an artificial dataset for Vietnamese Spelling Error correction tasks

## Introduction

In fact, there is now no public resource available for training the Vietnamese spelling error correction problem. 

In our paper, we propose a novel method for producing artificial errors from correct Vietnamese texts. The error is randomly generated in eight ways:

- Changes a character to another character in a word.
- Remove a character in a word.
- Swap the location of 2 characters in a word.
- Convert the true form of Vietnamese to telex form. Such as “ă” -> “aw”.
- Change a diacritic in a word, for instance, “á” -> “à”.
- Change the location of a diacritic in words, for example, “dứa" -> “dưá”.
- Split a true word into another two error words by space.
- Remove a word in a sentence.

## Create an artificial dataset

Following the below steps to auto-generate a dataset.

`Step 1:` Download the original Vietnamese dataset from [here](https://drive.google.com/drive/folders/1a4MJwEUn19P-LvxfDzAXz2zMv-d35L5a?fbclid=IwAR0J1hvuvIPcdTYxgWK8BAud42KObCfifJaAhQ1Gr6Fux-FY-l-YB7Fw4to). The dataset was random sampled from [binhvq dataset](https://github.com/binhvq/news-corpus)

`Step 2:` Unzip the dataset.

`Step 3:` Run the following command. The command will auto create a source file and a target file to the output folder.
```
$ python -m create_artificial_dataset.noise --input 'input_file.txt' --ouput 'output_folder'
```

**For examples:**

Using this command, the code will create 2 file in folder sample_data, includes `train.src` and `train.tgt`.
```
$ python -m create_artificial_dataset.noise --input sample_data/train.txt --output sample_data
```
