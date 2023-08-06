def n_gram_gen(sentence, gram):
    gram_list = []
    for word_index in range(len(sentence)):
        gram_list.append(sentence[word_index:word_index+gram])
    return gram_list



