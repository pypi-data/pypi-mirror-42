# -*- coding: utf-8 -*-
import os
from .text_classifier import TextClassifier

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
__VERSION__ = open(os.path.join(CURRENT_DIR, 'version.txt')).read()

__all__ = ['TextClassifier']
