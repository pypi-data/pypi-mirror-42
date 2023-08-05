# ReorientExpress

This is a script that is used to create, test and use models to predict the orientation of cDNA reads using deep neural networks.

----------------------------
# Table of Contents
----------------------------

   * [Overview](#overview)
   * [Installation](#installation)
   * [Commands and options](#commands-and-options)
   * [Usage example](#usage-example)
   
----------------------------
# Overview
----------------------------

ReorientExpress is a tool which main purpose is to predict the orientation of cDNA or RNA-direct reads. It builds kmer-based models using Deep Neural Networks and taking as input a transcriptome annotation or any other fasta/fasq file for which the sequences orientation is known. 
The software can work with experimental data, annotation data and also with mapped reads providing the corresponding PAF file. 
ReorientExpress has three main utilities:
- Training a model.
- Testing a model.
- Using a model to orient de input sequences.

SUPPA is a flexible and powerful tool to study splicing at the transcript isoform or at the local alternative splicing event level, across multiple conditions, and at high speed and accuracy. SUPPA has various modular operations that can be run separately to:

- Generate transcript events and local alternative splicing (AS) events from an annotation
- Quantify transcript and local AS event inclusion levels (PSIs) from multiple samples
- Calculate differential splicing for AS events and differential transcript.

----------------------------
# Installation
----------------------------

ReorientExpress has been developed in Python 3.6. 

Currently, you can use pip to do an authomatic installation:
```
pip3 install reorientexpress
```

If some dependencies are not correctly downloaded and installed, using the following can fix it:

```
pip3 install -r requirements.txt
pip3 install reorientexpress
```
Once the package is installed, ReorientExpress can be used from the command line as any other program.

----------------------------
# Commands and options
----------------------------

Once the package is installed it can be used as an independent program. ReorientExpress has three main functions, one of them must be provided when calling the program:

* -train: takes an input an uses it to train a model.
* -test: takes a model and a labeled input and tries the performance of the model in the input.
* -predict: takes a model and an input outputs all the sequences in forward. It also gives a certainty score. 

The different options that the program takes are:

* **-h, --help**:            Shows a help message with all the options.

*  **-train**:            Set true to train a model.

*  **-test**:                 Set true to test a model.

*  **-predict**:              Set true to use a model to make predictions

*  **-data D, --d D**:        The path to the input data. Must be either fasta or
                        fastq. Can be compressed in gz. Mandatory.
                        
*  **-source {annotation,experimental,mapped}, --s {annotation,experimental,mapped}**:
                        The source of the data. Must be either 'experimental',
                        'annotation' or 'mapped'. Choose experimental for
                        experiments like RNA-direct, annotation for
                        transcriptomes or other references and mapped for mapped
                        cDNA reads. Mapped reads require a paf file to know the
                        orientation. Mandatory.
                        
*  **-format {fasta,fastq,auto}, --f {fasta,fastq,auto}**:
                        The format of the input data. Auto by deafult. Change
                        only if inconsistencies in the name.
                        
*  **-annotation A, --a A**:  Path to the paf file if a mapped training set which
                        requires a paf reference is being used.
                        
*  **-use_all_annotation, -aa**:
                        Uses all the reads, instead of only keeping
                        antisense,lincRNA,processed_transcript,
                        protein_coding, and retained_intron. Use it also if
                        the fasta has unconventional format and gives errors.
                        
*  **-kmers K, --k K**:       The maximum length of the kmers used for training,
                        testing and using the models.
                        
*  **-reads R, --r R**:       Number of reads to read from the dataset.

*  **-trimming T, --t T**:    Number of nucleotides to trimm at each side. 0 by
                        default.
                        
*  **-verbose, --v**:         Whether to print detailed information about the
                        training process.
                        
*  **-epochs E, --e E**:      Number of epochs to train the model.

*  **-output O, --o O**:      Where to store the outputs. using "--train" outputs a
                        model, while using "-predict" outputs a csv.
                        Corresponding extensions will be added.

*  **-model M, --m M**:       The model to test or to predict with.

----------------------------
# Usage example
----------------------------

To train a model:

```
reorientexpress -train -data path_to_data -source annotation --v -output my_model
```

Which train a model with the data stored in path_to_data, which is an annotation file, suchs as a transcriptome and outputs a file called my_model.model which can be later used to make predictions. Prints relevant information.

To make predictions:

```
reorientexpress -predict -data path_to_data -source experimental -model path_to_model -output my_predictions
```

Which takes the experimental data stored in path_to_data and the model stored in path_to_model and converts to forward reads the reads that the model predicts are in reverse complementary, printing the results in my_predictions.csv. 

