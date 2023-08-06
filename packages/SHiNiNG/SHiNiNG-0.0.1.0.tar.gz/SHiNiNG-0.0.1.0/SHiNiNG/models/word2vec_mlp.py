from . import ShiningBuildInModel, ShiningSubModel
from ..tokenizer import tokenize, n_gram_gen
from keras.layers import Dense, Dropout
from keras.models import Sequential, load_model
from gensim.models import Word2Vec
import numpy as np

__author__ = 'LanYixiao_Eathoublu'


class Word2VecTrainingMaster(ShiningSubModel):
    def __init__(self, new_work=True,
                 corpus_path='',
                 work_path='.',
                 base_name='word2vec.model',
                 num_features=100,
                 min_word_count=1,
                 context=4, auto=True,
                 batch_size=100000,
                 step_save=True,
                 train_progress_bar=True,
                 tokenize_flag=1,
                 n_gram=3
                 ):
        super().__init__()
        self.work_path = work_path
        self.corpus_path = corpus_path
        self.word2vec_model = self.make_word2vec_model(num_features, min_word_count, context)
        self.base_name = base_name
        self.word2vec_model.save(self.work_path + '/' + self.base_name)
        self.step_save = step_save
        try:
            from tqdm import tqdm
        except:
            Warning('ImportError', 'tqdm package is missed. Progress bar cannot display. Try pip install tqdm.')
            train_progress_bar = False
        if auto:
            # with open(self.corpus_path) as f:
            #     reader = f.readlines()
            #     f.close()
            reader = corpus_path

            length = len(reader)
            model_init = True
            if train_progress_bar:
                for batch_index in tqdm(range(0, length, batch_size)):
                    batch = reader[batch_index: batch_index+batch_size]
                    batch = self.batch_compile(batch, tokenize_flag, n_gram)
                    self.update_model(batch, init=model_init)
                    model_init = False
            else:
                for batch_index in range(0, length, batch_size):
                    batch = reader[batch_index: batch_index+batch_size]
                    batch = self.batch_compile(batch, tokenize_flag, n_gram)
                    self.update_model(batch, init=model_init)
                    model_init = False
            self.word2vec_model.save(self.work_path + '/' + self.base_name)

    def make_word2vec_model(self, num_features, min_word_count, context):
        return Word2Vec(size=num_features, min_count=min_word_count, window=context)

    def update_model(self, batch, init):
        if self.step_save:
            self.word2vec_model = Word2Vec.load(self.work_path + '/' + self.base_name)
        if init:
            self.word2vec_model.build_vocab(batch)
        else:
            self.word2vec_model.build_vocab(batch, update=True)
        self.word2vec_model.train(batch, total_examples=self.word2vec_model.corpus_count, epochs=self.word2vec_model.iter)
        if self.step_save:
            self.word2vec_model.save(self.work_path + '/' + self.base_name)

    @staticmethod
    def batch_compile(batch, tokenize_flag, n_gram=3):
        sentence_list = []
        for sentence in batch:
            gram_list = tokenize.tokenizer(sentence) if tokenize_flag == 1 else n_gram_gen.n_gram_gen(sentence, n_gram)
            sentence_list.append(gram_list)
        return sentence_list


class VecTrainNnModelMaster(ShiningSubModel):
    def __init__(self, w2v_model_path='',
                 language_corpus='',
                 language_target='',
                 ks_model_name='ks.model',
                 batch_size=32,
                 auto=True,
                 ks_input_dim=300,
                 ks_train_batch=64,
                 ks_train_epoch=30,
                 ks_dense_1=64,
                 ks_dense_2=64,
                 ks_dense_3=5,
                 train_verbose=1,
                 use_generator=True,
                 tokenize_flag=1,
                 n_gram=3,
                 ):
        super().__init__()
        self.ks_cfg = {'ks_input_dim': ks_input_dim,
                       'ks_train_batch': ks_train_batch,
                       'ks_train_epoch': ks_train_epoch,
                       'ks_dense_1': ks_dense_1,
                       'ks_dense_2': ks_dense_2,
                       'ks_dense_3': ks_dense_3,
                       'train_verbose': train_verbose}
        self.use_generator = use_generator
        self.ks_model = self.make_ks_model(**self.ks_cfg)
        self.word2vec_model = Word2Vec.load(w2v_model_path)
        self.batch_size = batch_size
        self.ks_model_name = ks_model_name
        self.tokenize_flag=tokenize_flag
        self.n_gram=n_gram
        if auto:
            self.language_src = language_corpus
            self.language_tgt = language_target
            self.data_length = len(self.language_tgt)
            self.ks_train()

    def ks_train(self):
        # print(self.data_length, self.batch_size)
        if self.use_generator:
        # if len(self.language_tgt) >= 200000:
            self.ks_model.fit_generator(generator=self.make_batch(batch_size=self.batch_size),
                                        epochs=self.ks_cfg['ks_train_epoch'],
                                        validation_steps=self.make_batch(batch_size=32, validation=False),
                                        steps_per_epoch=self.data_length / self.batch_size,
                                        verbose=self.ks_cfg['train_verbose'])
        else:
            self.ks_model.fit(x=np.array(self.sen2vec(self.language_src[:3000])),
                              y=np.array(self.tar2one_hot(self.language_tgt[:3000])), batch_size=2, verbose=1, epochs=20)


        self.ks_model.save(self.ks_model_name)
        _, acc = self.ks_model.evaluate(x=np.array(self.sen2vec(self.language_src[3000:])), y=np.array(self.tar2one_hot(self.language_tgt[3000:])), verbose=0, batch_size=1)
        print('[info]Model trained successfully with accurancy~=%s, saved as:%s . If the acc is dissatisfactory, try change some parameters or shuffle the data.'%(str(acc)[:4], self.ks_model_name))

    def make_batch(self, batch_size, validation=False):
        for times in range(self.ks_cfg['ks_train_epoch']):
            if validation:
                try:
                    from tqdm import tqdm
                    for index in tqdm(range(0, 1000, batch_size)):
                        batch_sentence_list = self.language_src[index: index + batch_size]
                        sentences_vec_list = self.sen2vec(sen_list=batch_sentence_list)
                        target_list = self.language_tgt[index: index + batch_size]
                        target_list = self.tar2one_hot(target_list)
                        # target_list = [[0, 1] for _ in range(len(sentences_vec_list))]
                        yield ({'dense_1_input': np.array(sentences_vec_list)}, {'dense_3': np.array(target_list)})
                except:
                    Warning('ImportError', 'tqdm package is missed. Progress bar cannot display. Try pip install tqdm.')
                    for index in range(0, 1000, batch_size):
                        batch_sentence_list = self.language_src[index: index + batch_size]
                        sentences_vec_list = self.sen2vec(sen_list=batch_sentence_list)
                        target_list = self.language_tgt[index: index + batch_size]
                        target_list = self.tar2one_hot(target_list)
                        # target_list = [[0, 1] for _ in range(len(sentences_vec_list))]
                        yield ({'dense_1_input': np.array(sentences_vec_list)}, {'dense_3': np.array(target_list)})
            else:
                if len(self.language_tgt) != len(self.language_src):
                    raise Exception('LengthError:target length and source length is not same.', str(len(self.language_src))+'!='+str(len(self.language_tgt)))
                try:
                    from tqdm import tqdm
                    for index in tqdm(range(0, len(self.language_src), batch_size)):
                        batch_sentence_list = self.language_src[index: index+batch_size]
                        sentences_vec_list = self.sen2vec(sen_list=batch_sentence_list)
                        target_list = self.language_tgt[index: index+batch_size]
                        target_list = self.tar2one_hot(target_list)
                        # target_list = [[0, 1] for _ in range(len(sentences_vec_list))]
                        yield ({'dense_1_input': np.array(sentences_vec_list)}, {'dense_3': np.array(target_list)})
                except:
                    Warning('ImportError', 'tqdm package is missed. Progress bar cannot display. Try pip install tqdm.')
                    for index in range(0, len(self.language_src), batch_size):
                        batch_sentence_list = self.language_src[index: index + batch_size]
                        sentences_vec_list = self.sen2vec(sen_list=batch_sentence_list)
                        target_list = self.language_tgt[index: index + batch_size]
                        target_list = self.tar2one_hot(target_list)
                        # target_list = [[0, 1] for _ in range(len(sentences_vec_list))]
                        yield ({'dense_1_input': np.array(sentences_vec_list)}, {'dense_3': np.array(target_list)})

    def sen2vec(self, sen_list=[]):
        return_list = []
        if not sen_list:
            raise Exception('DataError:No sentence in list.', sen_list)
        for sentence in sen_list:
            sentence_vector = np.zeros((self.ks_cfg['ks_input_dim'], ))
            valid_gram = 0
            sentence_grams = tokenize.tokenizer(sentence) if self.tokenize_flag == 1 else n_gram_gen.n_gram_gen(sentence, self.n_gram)
            for gram in sentence_grams:
                if gram in self.word2vec_model:
                    valid_gram += 1
                    sentence_vector += self.word2vec_model[gram]
            if valid_gram != 0:
                sentence_vector /= valid_gram
            return_list.append(sentence_vector)
        return return_list
    def tar2one_hot(self, target_list):
        one_hot = np.zeros((len(target_list), 2))
        for index in range(len(target_list)):
          one_hot[index, int(target_list[index][:-1])] = 1
        return one_hot
    def make_ks_model(self, **kwargs):
        model = Sequential()
        model.add(Dense(kwargs['ks_dense_1'], input_dim=kwargs['ks_input_dim'], activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(kwargs['ks_dense_2'], activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(kwargs['ks_dense_3'], activation='softmax'))
        model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
        return model
    # @staticmethod
    # def read_file(file_name, mode='r'):
    #     return open(file_name, mode=mode).readlines()


class Word2vec_Mlp(ShiningBuildInModel):

    def __init__(self):
        super().__init__()

    def auto(self,
             w2v_model_path='w2v.model',
             language_corpus='',
             language_target='',
             ks_model_name='ks.model',
             ks_batch_size=1,
             auto=True,
             ks_input_dim=100,
             ks_train_batch=64,
             ks_train_epoch=20,
             ks_dense_1=64,
             ks_dense_2=64,
             ks_dense_3=2,
             new_work=True,
             corpus_path='',
             work_path='.',
             num_features=100,
             min_word_count=1,
             context=4,
             w2v_batch_size=100000,
             step_save=False,
             generator=True,
             train_progress_bar=True,
             train_verbose=0,
             tokenize_flag=1,
             n_gram=3,
             **kwargs):

        corpus_path = language_corpus
        base_name = w2v_model_path
        w2v_model_path = work_path + '/' + w2v_model_path
        ks_model_name =  work_path + '/' + ks_model_name

        self.handler_w2v(new_work=new_work,
                        corpus_path=corpus_path,
                        base_name=base_name,
                        work_path=work_path,
                        num_features=num_features,
                        min_word_count=min_word_count,
                        context=context,
                        auto=auto,
                        w2v_batch_size=w2v_batch_size,
                        step_save=step_save,
                        train_progress_bar=train_progress_bar,
                         tokenize_flag=tokenize_flag, n_gram=n_gram)
        #
        self.handler_mlp(w2v_model_path=w2v_model_path,
                        language_corpus=language_corpus,
                        language_target=language_target,
                        ks_model_name=ks_model_name,
                        ks_batch_size=ks_batch_size,
                        auto=auto,
                        ks_input_dim=ks_input_dim,
                        ks_train_batch=ks_train_batch,
                        ks_train_epoch=ks_train_epoch,
                        ks_dense_1=ks_dense_1,
                        ks_dense_2=ks_dense_2,
                        ks_dense_3=ks_dense_3,
                        train_verbose=train_verbose,
                        tokenize_flag=tokenize_flag, n_gram=n_gram
                         )

    def handler_w2v(self, new_work=True,
                 corpus_path='',
                 work_path='.',
                 base_name='word2vec.model',
                 num_features=300,
                 min_word_count=1,
                 context=4,
                 auto=True,
                 w2v_batch_size=100000,
                 step_save=False,
                 train_progress_bar=True,
                 tokenize_flag=1,
                 n_gram=3):
        self.word2vec_train = Word2VecTrainingMaster(
            new_work=new_work,
            corpus_path=corpus_path,
            base_name=base_name,
            work_path=work_path,
            num_features=num_features,
            min_word_count=min_word_count,
            context=context,
            auto=auto,
            batch_size=w2v_batch_size,
            step_save=step_save,
            train_progress_bar=train_progress_bar,
            tokenize_flag=tokenize_flag,
            n_gram=n_gram

        )

    def handler_mlp(self,
                 w2v_model_path='',
                 language_corpus='',
                 language_target='',
                 ks_model_name='ks.model',
                 ks_batch_size=32,
                 auto=True,
                 ks_input_dim=300,
                 ks_train_batch=64,
                 ks_train_epoch=30,
                 ks_dense_1=64,
                 ks_dense_2=64,
                 ks_dense_3=2,
                 train_verbose=1,
                 tokenize_flag=1,
                 n_gram=3):
        self.mlp_train = VecTrainNnModelMaster(
            w2v_model_path=w2v_model_path,
            language_corpus=language_corpus,
            language_target=language_target,
            ks_model_name=ks_model_name,
            batch_size=ks_batch_size,
            auto=auto,
            ks_input_dim=ks_input_dim,
            ks_train_batch=ks_train_batch,
            ks_train_epoch=ks_train_epoch,
            ks_dense_1=ks_dense_1,
            ks_dense_2=ks_dense_2,
            ks_dense_3=ks_dense_3,
            train_verbose=train_verbose,
            tokenize_flag=tokenize_flag,
            n_gram=n_gram,
        )

    def predict(self, src_reader, output_index, confidence, one_hot, tokenize_falg=1, ks_model='ks.model', w2v_model='w2v.model',):
        try:
            from tqdm import tqdm
        except:
            Warning('ImportError', 'tqdm is needed to display progress bar, please pip install tqdm.')
        ks_model = load_model(ks_model)
        w2v_model = Word2Vec.load(w2v_model)
        for sentence in tqdm(src_reader):
            grams = tokenize.tokenizer(sentence) if tokenize_falg == 1 else n_gram_gen.n_gram_gen(sentence)
            valid = 0
            sentence_vec = np.zeros((100, ))
            for gram in grams:
                if gram in w2v_model:
                    sentence_vec += w2v_model[gram]
                    valid += 1
                if valid != 0:
                    sentence_vec /= valid
            res = ks_model.predict(np.array([sentence_vec]))[0].tolist()
            if one_hot:
                output_index.write(str(res)+' ')
            else:
                output_index.write(str(res.index(max(res)))+' ')
            if confidence:
                output_index.write(str(res[0]/res[1] if res[0]>res[1] else res[1]/res[0]))
            output_index.write('\n')
        output_index.close()
        return



























