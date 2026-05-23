from typing import Any, Dict, Tuple, List
import logging
import torch
import torch.nn as nn
from pandas import DataFrame
import torch.optim as optim
from freqtrade.freqai.base_models.BasePyTorchClassifier import BasePyTorchClassifier
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.torch.PyTorchDataConvertor import (
    DefaultPyTorchDataConvertor,
    PyTorchDataConvertor,
)
from freqtrade.freqai.torch.PyTorchMLPModel import PyTorchMLPModel
from freqtrade.freqai.torch.PyTorchModelTrainer import PyTorchModelTrainer


from LSTMClassifier import LSTMClassifier


class ZHU_LSTMTradeClassifier02h(BasePyTorchClassifier):
    @property
    def data_convertor(self) -> PyTorchDataConvertor:
        return DefaultPyTorchDataConvertor(
            target_tensor_type=torch.long, squeeze_target_tensor=True
        )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        config = self.freqai_info.get("model_training_parameters", {})

        self.model_kwargs: Dict[str, Any] = config.get("model_kwargs", {})
        self.hidden_size = self.model_kwargs.get("hidden_size", 768)
        self.num_layers = self.model_kwargs.get("num_layers", 4)
        self.dropout_rate = self.model_kwargs.get("dropout_rate", 0.2)
        self.learning_rate: float = self.model_kwargs.get(
            "learning_rate", 0.001)

        self.trainer_kwargs: Dict[str, Any] = config.get("trainer_kwargs", {})

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        class_names = self.get_class_names()
        self.convert_label_column_to_int(data_dictionary, dk, class_names)
        n_features = data_dictionary["train_features"].shape[-1]

        model = LSTMClassifier(
            input_size=n_features,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            num_classes=len(class_names),
            dropout_rate=self.dropout_rate
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.CrossEntropyLoss()
        trainer = self.get_init_model(dk.pair)
        if trainer is None:
            trainer = PyTorchModelTrainer(
                model=model,
                optimizer=optimizer,
                criterion=criterion,
                model_meta_data={"class_names": class_names},
                device=self.device,
                data_convertor=self.data_convertor,
                tb_logger=self.tb_logger,
                **self.trainer_kwargs,
            )
        trainer.fit(data_dictionary, self.splits)
        return trainer
