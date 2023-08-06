# encoding: utf-8
"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz

@version: 1.0
@license: Apache Licence
@file: blstm_attention_model
@time: 2019-01-31

"""
import logging

import numpy as np
from keras.layers import Bidirectional, LSTM, Embedding, Input, RepeatVector
from keras.layers import Dense, Dropout, TimeDistributed, Activation
from keras.models import Model, Sequential

from kashgari.tasks.seq_labeling.base_model import SequenceLabelingModel
import keras
from keras import backend as k
from keras.preprocessing.text import Tokenizer
from keras import initializers
from keras.optimizers import RMSprop
from keras.models import Sequential,Model
from keras.layers import Dense,LSTM,Dropout,Input,Activation,Add,Concatenate
from keras.layers.advanced_activations import LeakyReLU,PReLU
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras.optimizers import Adam


class BLSTMAttentionModel(SequenceLabelingModel):
    __architect_name__ = 'BLSTMAttentionModel'
    __base_hyper_parameters__ = {}

    def build_model(self, loss_f=None, optimizer=None, metrics=None, **kwargs):
        encoder_inputs = Input(shape=self.embedding.model.input_shape)

        encoder_LSTM = LSTM(64, dropout_U=0.2, dropout_W=0.2, return_state=True)
        encoder_LSTM_rev = LSTM(64, return_state=True, go_backwards=True)

        # merger=Add()[encoder_LSTM(encoder_inputs), encoder_LSTM_rev(encoder_inputs)]
        encoder_outputsR, state_hR, state_cR = encoder_LSTM_rev(encoder_inputs)
        encoder_outputs, state_h, state_c = encoder_LSTM(encoder_inputs)

        state_hfinal = Add()([state_h, state_hR])
        state_cfinal = Add()([state_c, state_cR])

        encoder_states = [state_hfinal, state_cfinal]

        """____decoder___"""
        decoder_inputs = Input(shape=self.embedding.model.input_shape)
        decoder_LSTM = LSTM(64, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_LSTM(decoder_inputs, initial_state=encoder_states)
        decoder_dense = Dense(len(self.label2idx), activation='linear')
        decoder_outputs = decoder_dense(decoder_outputs)

        model = Model(inputs=[encoder_inputs, decoder_inputs], outputs=decoder_outputs)
        # plot_model(model, to_file=modelLocation+'model.png', show_shapes=True)
        rmsprop = RMSprop(lr=0.004, clipnorm=1.0)

        model.compile(loss='mse', optimizer=rmsprop)

        self.model = model
        self.model.summary()


if __name__ == '__main__':
    import random
    from keras.callbacks import ModelCheckpoint
    from kashgari.utils.logger import init_logger
    from kashgari.corpus import ChinaPeoplesDailyNerCorpus

    init_logger()
    x_train, y_train = ChinaPeoplesDailyNerCorpus.get_sequence_tagging_data()
    x_validate, y_validate = ChinaPeoplesDailyNerCorpus.get_sequence_tagging_data(data_type='validate')
    x_test, y_test = ChinaPeoplesDailyNerCorpus.get_sequence_tagging_data(data_type='test')

    # embedding = WordEmbeddings('sgns.weibo.bigram', sequence_length=100)
    m = BLSTMAttentionModel()
    check = ModelCheckpoint('./model.model',
                            monitor='acc',
                            verbose=1,
                            save_best_only=False,
                            save_weights_only=False,
                            mode='auto',
                            period=1)
    m.fit(x_train[:1000],
          y_train[:1000],
          class_weight=True,
          epochs=1,
          y_validate=y_validate,
          x_validate=x_validate,
          labels_weight=False)

    sample_queries = random.sample(list(range(len(x_train))), 10)
    for i in sample_queries:
        text = x_train[i]
        logging.info('-------- sample {} --------'.format(i))
        logging.info('x: {}'.format(text))
        logging.info('y_true: {}'.format(y_train[i]))
        logging.info('y_pred: {}'.format(m.predict(text)))
    logging.info(m.predict(list('总统特朗普今天在美国会见了朝鲜领导金正恩'), debug_info=True))
    m.evaluate(x_test, y_test, debug_info=True)
