# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Exporting ModeKeys to tf.estimator namespace."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.util.tf_export import estimator_export


# TODO(kathywu): use mode keys defined in saved_model/model_utils/mode_keys,
# and combine ModeKeys and ModeKeysV2.
@estimator_export('estimator.ModeKeys', v1=[])
class ModeKeysV2(object):
  """Standard names for model modes.

  The following standard keys are defined:

  * `TRAIN`: training/fitting mode.
  * `EVAL`: testing/evaluation mode.
  * `PREDICT`: predication/inference mode.
  """

  TRAIN = 'train'
  EVAL = 'eval'
  PREDICT = 'infer'
