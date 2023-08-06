#   _____ _    _ _ _   _ _ _   _  _____
#  / ____| |  | (_) \ | (_) \ | |/ ____|
# | (___ | |__| |_|  \| |_|  \| | |  __
#  \___ \|  __  | | . ` | | . ` | | |_ |
#  ____) | |  | | | |\  | | |\  | |__| |
# |_____/|_|  |_|_|_| \_|_|_| \_|\_____|
#
#    -- * Lan-Yixiao * Eathoublu * --
#          -- Source Code NLP --
#
#  The easiest and powerful deep-learning-text-classifier
#  For human beings and all purposes.

from .models.word2vec_mlp import Word2vec_Mlp
from .models import ShiningBuildInModel
from .rand import random_in_memory, random_in_disk
import os
from time import time

__author__ = 'LanYixiao_Eathoublu'

__all__ = ['Shining']


class Shining(object):

    def __init__(self, hi='Welcome use SHiNiNG nlp toolkit.',
                 maximum_data_in_memory=200000,
                 work_path=os.path.abspath('.'),
                 ):
        self.__work_path = work_path
        self.__mdim = maximum_data_in_memory

    def train_from_file(self, text_src, tag_src,
                        output_model_path='.',
                        train_model='word2vec+MLP',
                        randomize=True,
                        train_with_generator=True,
                        tokenize_mode='tokenize',
                        n_gram=3,
                        train_verbose=0,
                        train_progress_bar=True,
                        train_epoch=20,
                        train_batch_size=2,
                        **kwargs):
        print('[info]Process start.')
        t1 = time()
        if not train_with_generator:
            Warning('[Warning]', 'Only support train with generator in this version.')
        if isinstance(train_model, str):
            if train_model == 'word2vec+MLP':
                model = Word2vec_Mlp()
            else:
                model = ShiningBuildInModel()
        elif isinstance(train_model, ShiningBuildInModel):
                # model = train_model()
                pass
        else:
            raise Exception('ModelError', 'train_model should be a string like "word2vec+MLP" or a instance of ShiningBuildInModel')
        f_data = open(text_src).readlines()
        f_tag = open(tag_src).readlines()
        if randomize:
            if len(f_data) != len(f_tag):
                raise Exception('LengthError',
                                'len(text) should equal to len(tag) got:%d and %d' % (len(f_data), len(f_tag)))
            length = len(f_data)
            if length <= self.__mdim:
                X, y = self.__random_in_memory(f_data, f_tag)
            else:
                if not train_with_generator:
                    raise Exception('LengthError',
                                    'Data length is too long(%d>%d). Train with generator.' % (length, self.__mdim))
                X, y = self.__random_in_disk(f_data, f_tag)
        else:
            X, y = f_data, f_tag

        if tokenize_mode == 'tokenize':
            tokenize_flag = 1
        elif tokenize_mode == 'n-gram':
            tokenize_flag = 2
        else:
            raise Exception('ModeError', 'tokenize_mode can only be set to "tokenize" or "n-gram".')
        print('[info]Pre-train process ready.The train progress would take some times, please wait...')
        self.__train(model=model, dat=X, tag=y,
                   output_model_path=output_model_path,
                   tokenize_flag=tokenize_flag,
                   generator=train_with_generator,
                   train_verbose=train_verbose,
                   train_progress_bar=train_progress_bar,
                   work_path=self.__work_path,
                   n_gram=n_gram,
                   train_epoch=train_epoch,
                   ks_batch_size=train_batch_size,
                     )
        print('[info]Train finish in time:%sS.' % (str(time() - t1)[:4],))

    def predict_to_file(self, src_file_path,
                          output_file_path='output.txt',
                          w2v_model='w2v.model',
                          ks_model='ks.model',
                          tokenize_mode='tokenize',
                          mode='word2vec+mlp',
                          confidence=True,
                          one_hot=False
                          ):
        t2 = time()
        w2v_model = self.__work_path + '/' + w2v_model
        ks_model = self.__work_path + '/' + ks_model
        if mode == 'word2vec+mlp':
            model = Word2vec_Mlp()
        if tokenize_mode == 'tokenize':
            tokenize_flag = 1
        elif tokenize_mode == 'n-gram':
            tokenize_flag = 2
        else:
            raise Exception('ModeError', 'tokenize_mode can only be set to "tokenize" or "n-gram".')
        model.predict(open(src_file_path).readlines(),
                      output_index=open(output_file_path, 'a'),
                      tokenize_falg=tokenize_flag,
                      w2v_model=w2v_model,
                      ks_model=ks_model,
                      confidence=confidence,
                      one_hot=one_hot,
                      )
        print('[info]Output result has been saved in:%s .'%(output_file_path, ))
        print('[info]Train finish in time:%sS.' % (str(time() - t2)[:4],))


    @staticmethod
    def __random_in_memory(dat, tag):
        return random_in_memory(dat, tag)

    @staticmethod
    def __random_in_disk(dat, tag):
        return random_in_disk(dat, tag)

    @staticmethod
    def __train(model, dat, tag,
                output_model_path,
                tokenize_flag,
                generator=False,
                train_verbose=0,
                train_progress_bar=True,
                work_path='',
                n_gram=3,
                **kwargs
                ):

        model.auto(
             language_corpus=dat,
             language_target=tag,
             auto=True,
             work_path=work_path,
             step_save=False,
             train_verbose=train_verbose,
             tokenize_flag=tokenize_flag,
             n_gram=n_gram,
             train_progress_bar=train_progress_bar,
             generator=generator,
             ks_train_epoch=kwargs['train_epoch'],
             output_model_path=output_model_path,
             ks_batch_size=kwargs['ks_batch_size']
        )

if __name__ == '__main__':

    sng = Shining()

    # sng.train_from_file(text_src='all', tag_src='tag', output_model_path='.')

    sng.predict_to_file('all',)




















