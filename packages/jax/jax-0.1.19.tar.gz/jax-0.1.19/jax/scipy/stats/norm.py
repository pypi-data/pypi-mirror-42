# Copyright 2018 Google LLC
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as onp
import scipy.stats as osp_stats

from ... import lax
from ...numpy.lax_numpy import _promote_args_like, _constant_like, _wraps


@_wraps(osp_stats.norm.logpdf)
def logpdf(x, loc=0, scale=1):
  x, loc, scale = _promote_args_like(osp_stats.norm.logpdf, x, loc, scale)
  two = _constant_like(x, 2)
  scale_sqrd = lax.pow(scale, two)
  log_normalizer = lax.log(lax.mul(_constant_like(x, 2 * onp.pi), scale_sqrd))
  quadratic = lax.div(lax.pow(lax.sub(x, loc), two), scale_sqrd)
  return lax.div(lax.neg(lax.add(log_normalizer, quadratic)), two)

@_wraps(osp_stats.norm.pdf)
def pdf(x, loc=0, scale=1):
  return lax.exp(logpdf(x, loc, scale))
