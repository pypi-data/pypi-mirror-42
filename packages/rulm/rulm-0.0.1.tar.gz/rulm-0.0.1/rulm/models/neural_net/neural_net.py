import os
from typing import List, Tuple, Iterable, Dict
import logging

import torch
from torch import Tensor
import numpy as np
from allennlp.common.params import Params
from allennlp.training.trainer import Trainer
from allennlp.data.vocabulary import Vocabulary
from allennlp.data.iterators.data_iterator import DataIterator
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.models.model import Model

from rulm.transform import Transform
from rulm.language_model import LanguageModel

logger = logging.getLogger(__name__)


@LanguageModel.register("neural_net")
class NeuralNetLanguageModel(LanguageModel):
    def __init__(self,
                 vocab: Vocabulary,
                 model: Model,
                 transforms: Tuple[Transform]=None,
                 reader: DatasetReader = None):
        LanguageModel.__init__(self, vocab, transforms, reader)

        self.model = model
        self.log_model()

    def train(self,
              train_file_name: str,
              train_params: Params,
              serialization_dir: str = None,
              valid_file_name: str = None):
        assert os.path.exists(train_file_name)
        assert not valid_file_name or os.path.exists(valid_file_name)
        train_dataset = self.reader.read(train_file_name)
        valid_dataset = self.reader.read(valid_file_name) if valid_file_name else None

        iterator = DataIterator.from_params(train_params.pop('iterator'))
        iterator.index_with(self.vocab)
        trainer = Trainer.from_params(self.model, serialization_dir, iterator,
                                      train_dataset, valid_dataset, train_params.pop('trainer'))
        train_params.assert_empty("Trainer")
        return trainer.train()

    def predict(self,
                batch: Dict[str, Dict[str, Tensor]],
                temperature: float=1.0) -> List[List[float]]:
        self.model.eval()
        output_dict = self.model.forward(**batch)
        logits = output_dict["logits"]
        logits = logits.div(temperature)
        result = torch.exp(logits[:, -1])
        result_norm = torch.nn.functional.normalize(result, p=1)
        result = result_norm.cpu().detach().numpy()
        return result

    def log_model(self):
        logger.info(self.model)
        params_count = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        logger.info("Trainable params count: " + str(params_count))

    @classmethod
    def _load(cls,
              params: Params,
              vocab: Vocabulary,
              serialization_dir: str,
              weights_file: str,
              cuda_device: int=-1,
              **kwargs):
        if params.get('train', None):
            params.pop('train')

        inner_model = Model.load(
            params,
            serialization_dir,
            weights_file=weights_file,
            cuda_device=cuda_device)
        params.pop('model')
        if params.get('vocabulary', None):
            params.pop('vocabulary')
        model = NeuralNetLanguageModel.from_params(params, model=inner_model, vocab=vocab, **kwargs)
        return model

