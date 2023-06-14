# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from absl.testing import absltest
from weatherbench2 import schema
from weatherbench2 import utils
import xarray


class UtilsTest(absltest.TestCase):

  def testMethodEquivalence(self):
    """Test whether explicit and fast methods are equivalent for mean without leap year."""
    truth = schema.mock_truth_data(
        variables_3d=[],
        variables_2d=['2m_temperature'],
        time_start='2022-01-01',
        time_stop='2023-01-01',
    ).drop('level')
    truth = truth + 1 * truth.time.dt.dayofyear
    explicit = utils.compute_hourly_stat(
        truth,
        window_size=61,
        clim_years=slice(None, None),
        hour_interval=24,
        stat_fn='mean',
    )
    fast = utils.compute_hourly_stat_fast(
        truth,
        window_size=61,
        clim_years=slice(None, None),
        hour_interval=24,
        stat_fn='mean',
    )
    xarray.testing.assert_allclose(explicit, fast)


if __name__ == '__main__':
  absltest.main()
