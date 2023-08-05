# coding=utf-8
# Copyright 2019 The TensorFlow Datasets Authors.
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

"""Tests for tensorflow_datasets.core.dataset_info."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import tempfile
import numpy as np
import tensorflow as tf

from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import features
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.image import mnist
import tensorflow_datasets.testing as tfds_test

tf.compat.v1.enable_eager_execution()

_TFDS_DIR = py_utils.tfds_dir()
_INFO_DIR = os.path.join(_TFDS_DIR, "testing", "test_data", "dataset_info",
                         "mnist", "1.0.0")
_NON_EXISTENT_DIR = os.path.join(_TFDS_DIR, "non_existent_dir")


DummyDatasetSharedGenerator = tfds_test.DummyDatasetSharedGenerator


class RandomShapedImageGenerator(DummyDatasetSharedGenerator):

  def _info(self):
    return dataset_info.DatasetInfo(
        builder=self,
        features=features.FeaturesDict({"im": features.Image()}),
        supervised_keys=("im", "im"),
    )

  def _generate_examples(self):
    for _ in range(30):
      height = np.random.randint(5, high=10)
      width = np.random.randint(5, high=10)
      yield {
          "im":
              np.random.randint(
                  0, 255, size=(height, width, 3), dtype=np.uint8)
      }


class DatasetInfoTest(tfds_test.TestCase):

  @classmethod
  def setUpClass(cls):
    super(DatasetInfoTest, cls).setUpClass()
    cls._tfds_tmp_dir = tfds_test.make_tmp_dir()
    cls._builder = DummyDatasetSharedGenerator(data_dir=cls._tfds_tmp_dir)

  @classmethod
  def tearDownClass(cls):
    tfds_test.rm_tmp_dir(cls._tfds_tmp_dir)

  def test_undefined_dir(self):
    with self.assertRaisesWithPredicateMatch(ValueError,
                                             "undefined dataset_info_dir"):
      info = dataset_info.DatasetInfo(builder=self._builder)
      info.read_from_directory(None)

  def test_non_existent_dir(self):
    info = dataset_info.DatasetInfo(builder=self._builder)
    info.read_from_directory(_NON_EXISTENT_DIR)

    self.assertFalse(info.initialized)

  def test_reading(self):
    info = dataset_info.DatasetInfo(builder=self._builder)
    info.read_from_directory(_INFO_DIR)

    # Assert that we read the file and initialized DatasetInfo.
    self.assertTrue(info.initialized)
    self.assertTrue("mnist", info.name)

    # Test splits are initialized properly.
    split_dict = info.splits

    # Assert they are the correct number.
    self.assertTrue(len(split_dict), 2)

    # Assert on what they are
    self.assertTrue("train" in split_dict)
    self.assertTrue("test" in split_dict)

    # Assert that this is computed correctly.
    self.assertEqual(70000, info.splits.total_num_examples)

    self.assertEqual("image", info.supervised_keys[0])
    self.assertEqual("label", info.supervised_keys[1])

  def test_writing(self):
    # First read in stuff.
    info = dataset_info.DatasetInfo(builder=self._builder)
    info.read_from_directory(_INFO_DIR)

    # Read the json file into a string.
    with tf.io.gfile.GFile(info._dataset_info_filename(_INFO_DIR)) as f:
      existing_json = json.load(f)

    # Now write to a temp directory.
    with tfds_test.tmp_dir(self.get_temp_dir()) as tmp_dir:
      info.write_to_directory(tmp_dir)

      # Read the newly written json file into a string.
      with tf.io.gfile.GFile(info._dataset_info_filename(tmp_dir)) as f:
        new_json = json.load(f)

    # Assert what was read and then written and read again is the same.
    self.assertEqual(existing_json, new_json)

  def test_reading_from_gcs_bucket(self):
    mnist_builder = mnist.MNIST(
        data_dir=tempfile.mkdtemp(dir=self.get_temp_dir()))
    info = dataset_info.DatasetInfo(builder=mnist_builder)
    info = mnist_builder.info

    # A nominal check to see if we read it.
    self.assertTrue(info.initialized)
    self.assertEqual(10000, info.splits["test"].num_examples)

  def test_str_smoke(self):
    info = mnist.MNIST(data_dir="/tmp/some_dummy_dir").info
    _ = str(info)

  @tfds_test.run_in_graph_and_eager_modes()
  def test_statistics_generation(self):
    with tfds_test.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = DummyDatasetSharedGenerator(data_dir=tmp_dir)
      builder.download_and_prepare()

      # Overall
      self.assertEqual(30, builder.info.splits.total_num_examples)

      # Per split.
      test_split = builder.info.splits["test"].get_proto()
      train_split = builder.info.splits["train"].get_proto()
      self.assertEqual(10, test_split.statistics.num_examples)
      self.assertEqual(20, train_split.statistics.num_examples)

  @tfds_test.run_in_graph_and_eager_modes()
  def test_statistics_generation_variable_sizes(self):
    with tfds_test.tmp_dir(self.get_temp_dir()) as tmp_dir:
      builder = RandomShapedImageGenerator(data_dir=tmp_dir)
      builder.download_and_prepare()

      # Get the expected type of the feature.
      schema_feature = builder.info.as_proto.schema.feature[0]
      self.assertEqual("im", schema_feature.name)

      self.assertEqual(-1, schema_feature.shape.dim[0].size)
      self.assertEqual(-1, schema_feature.shape.dim[1].size)
      self.assertEqual(3, schema_feature.shape.dim[2].size)

  def test_updates_on_bucket_info(self):

    info = dataset_info.DatasetInfo(builder=self._builder,
                                    description="won't be updated")
    # No statistics in the above.
    self.assertEqual(0, info.splits.total_num_examples)
    self.assertEqual(0, len(info.as_proto.schema.feature))

    # Partial update will happen here.
    info.read_from_directory(_INFO_DIR, from_bucket=True)

    # Assert that description (things specified in the code) didn't change
    # but statistics are updated.
    self.assertEqual("won't be updated", info.description)

    # These are dynamically computed, so will be updated.
    self.assertEqual(70000, info.splits.total_num_examples)
    self.assertEqual(2, len(info.as_proto.schema.feature))


if __name__ == "__main__":
  tfds_test.test_main()
