# -*- coding: utf-8 -*-
"""multitask_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rd1_yleruBJ9UCTM1DIycEfErpqCoDyn
"""

import torch
import torch.nn as nn
from models.sentence_transformer import SentenceTransformer  # Ensure this path is correct

class MultiTaskModel(nn.Module):
    """
    A multi-task model that expands the SentenceTransformer for two tasks:
      - Task A: Sentence Classification.
      - Task B: Sentiment Analysis.

    This model leverages a shared encoder (the SentenceTransformer) to generate fixed-length
    sentence embeddings, which are then processed by two task-specific heads.
    """

    def __init__(self, pretrained_model_name='bert-base-uncased', num_classes_taskA=3, num_classes_taskB=2):
        """
        Initializes the MultiTaskModel.

        Args:
            pretrained_model_name (str): Name of the pre-trained BERT model.
            num_classes_taskA (int): Number of classes for sentence classification.
            num_classes_taskB (int): Number of classes for sentiment analysis.
        """
        super(MultiTaskModel, self).__init__()
        # Shared encoder: reuse the SentenceTransformer from Task 1.
        self.encoder = SentenceTransformer(pretrained_model_name)
        hidden_size = self.encoder.transformer.config.hidden_size

        # Task A: Sentence Classification Head.
        self.classification_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, num_classes_taskA)
        )

        # Task B: Sentiment Analysis Head.
        self.sentiment_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, num_classes_taskB)
        )

    def forward(self, input_sentences):
        """
        Forward pass for the multi-task model.

        Args:
            input_sentences (list): A list of input sentence strings.

        Returns:
            tuple: (logits_taskA, logits_taskB) where:
                - logits_taskA: Logits from the sentence classification head.
                - logits_taskB: Logits from the sentiment analysis head.
        """
        # Generate sentence embeddings using the shared encoder.
        embeddings = self.encoder(input_sentences)

        # Process embeddings through each task-specific head.
        logits_taskA = self.classification_head(embeddings)
        logits_taskB = self.sentiment_head(embeddings)

        return logits_taskA, logits_taskB