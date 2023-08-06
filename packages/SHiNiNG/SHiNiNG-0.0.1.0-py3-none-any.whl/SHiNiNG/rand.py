from random import shuffle, random


__author__ = 'LanYixiao_Eathoublu'


def random_in_memory(dat, tag):
    union = zip(dat, tag)
    union = [item for item in union]
    shuffle(union)
    dat[:], tag[:] = zip(*union)
    return dat, tag


def random_in_disk(dat, tag):
    output_data = open('tmp.rand.dat', 'a')
    output_target = open('tmp.rand.tag', 'a')
    while dat and tag:
        length = len(dat)
        index = int(length*random())
        data = dat.pop(index)
        target = tag.pop(index)
        output_data.write(data)
        output_target.write(target)
    output_data.close()
    output_target.close()
    return open('tmp.rand.dat').readlines(), open('tmp.rand.tag').readlines()




