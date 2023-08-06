import jieba


def tokenizer(sentence):
    return [token for token in jieba.cut(sentence)]