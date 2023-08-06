# -*- coding: utf-8 -*-
"""NLP Tagger Tools built by pyTorch

.. moduleauthor:: Infinity Future <infinityfuture@foxmaill>

"""

import os
from .tagger import Tagger
from .torch_lm import START_TAG, STOP_TAG, PAD_TAG, UNK_TAG

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
__VERSION__ = open(os.path.join(CURRENT_DIR, 'version.txt')).read()

__all__ = ['Tagger', 'START_TAG', 'STOP_TAG', 'PAD_TAG', 'UNK_TAG']
