# MABLE - Better Together: Automated App Review Analysis with Deep Multi-task Learning
Dataset and replication package for the paper ***Better Together: Automated App Review Analysis with Deep Multi-task Learning***.

## Requirements
- Python 3.6
- Main libraries: requirements.txt
- [Pre-trained BERT](https://huggingface.co/bert-base-uncased)
	- Path: pytorch_version/prev_trained_model/

## Data
### Dataset Directory
The directory ```dataset``` is for the convenience of viewing the data. \
The dataset directory when running our code: ```pytorch_version/CLUEdatasets/cluener/```

### Data Field Format
```
id: Review ID
app: App name
text: Review sentence
senti: Sentence sentiment (negative: [-5, -1], positive: [1, 5])
type: Bug type of the current app review.
label: The problematic feature phrase, the beginning position and the ending position
```

## Usage
### Bug Classification & Problematic Feature Extraction
```angular2html
run_ner_crf.sh
```

You can change the configures in `run_ner_crf.sh`, including the `learning_rate`, `per_gpu_train_batch_size`, `per_gpu_eval_batch_size`, `num_train_epochs`, etc. The other important parameters are
```
overwrite_output_dir -- whether overwrite the output directory
do_train -- whether train the model
do_eval -- whether evluate the model
do_predict -- whether predict the results of new data
```

## Output
### Output Directory
```angular2html
pytorch_version/outputs/cluener_output/bert/
```
