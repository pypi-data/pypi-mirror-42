from unittest import TestCase
import torch
import keras
import numpy as np
from keras_pos_embd import TrigPosEmbedding
from torch_position_embedding import TrigonometricPositionEmbedding


class TestTrigonometricPositionEmbedding(TestCase):

    @staticmethod
    def gen_torch_net(embed_dim, mode):
        return TrigonometricPositionEmbedding(embedding_dim=embed_dim, mode=mode)

    @staticmethod
    def gen_keras_net(input_shape, embed_dim, mode):
        input_layer = keras.layers.Input(shape=input_shape)
        embed_layer = TrigPosEmbedding(mode=mode, output_dim=embed_dim)(input_layer)
        model = keras.models.Model(inputs=input_layer, outputs=embed_layer)
        model.compile(optimizer='adam', loss='mse')
        return model

    def test_mode_expand(self):
        torch_net = self.gen_torch_net(embed_dim=12, mode=TrigonometricPositionEmbedding.MODE_EXPAND)
        keras_net = self.gen_keras_net(input_shape=(None,), embed_dim=12, mode=TrigPosEmbedding.MODE_EXPAND)
        x = torch.randint(0, 100, (3, 7))
        torch_y = torch_net(x)
        keras_y = keras_net.predict(x.numpy())
        self.assertTrue(np.allclose(keras_y, torch_y.numpy(), rtol=0.0, atol=1e-4), (keras_y, torch_y.numpy()))

    def test_mode_add(self):
        torch_net = self.gen_torch_net(embed_dim=12, mode=TrigonometricPositionEmbedding.MODE_ADD)
        keras_net = self.gen_keras_net(input_shape=(None, 12), embed_dim=12, mode=TrigPosEmbedding.MODE_ADD)
        x = torch.randn(3, 7, 12)
        torch_y = torch_net(x)
        keras_y = keras_net.predict(x.numpy())
        self.assertTrue(np.allclose(keras_y, torch_y.numpy(), rtol=0.0, atol=1e-4), (keras_y, torch_y.numpy()))

    def test_mode_concat(self):
        torch_net = self.gen_torch_net(embed_dim=12, mode=TrigonometricPositionEmbedding.MODE_CONCAT)
        keras_net = self.gen_keras_net(input_shape=(None, 9), embed_dim=12, mode=TrigPosEmbedding.MODE_CONCAT)
        x = torch.randn(3, 7, 9)
        torch_y = torch_net(x)
        keras_y = keras_net.predict(x.numpy())
        self.assertTrue(np.allclose(keras_y, torch_y.numpy(), rtol=0.0, atol=1e-4), (keras_y, torch_y.numpy()))

    def test_mode_invalid(self):
        with self.assertRaises(NotImplementedError):
            net = self.gen_torch_net(embed_dim=10, mode='INVALID')
            print(net)
            x = torch.randn(3, 4, 6)
            net(x)
