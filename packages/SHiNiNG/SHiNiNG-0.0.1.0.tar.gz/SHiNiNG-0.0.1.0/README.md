# SHiNiNG nlp toolkit
## The easiest and powerful deep-learning-text-classifier for human beings and all purposes.
## AUTHOR - Lan-Yixiao Eathoublu From Northeastern University Shenyang China.
## Contact: 1012950361@qq.com


## Introduce

This is a lightweight nlp toolkit based on keras, tensorflow, gensim and jieba. So you should install these package at first.
It provided only two APIs which is the easiest and powerful way for users to train there model and use it in production environment for all purposes.


## How to use it?
To use it is easy.
```python

import SHiNiNG

sng = SHiNiNG.Shining()  # get instance of Shining.

```

There’s only two APIs.

```python
Shining().train_from_file(text_src='', tag_src='')  # get data and target split by ‘\n’ in files, you should run this method first to get trained model to predict. All of it is automatically done.
Shining().predict_from_file(src_file_path='')  # get data need to be predict from file, and get the target in ‘output.txt’

```





