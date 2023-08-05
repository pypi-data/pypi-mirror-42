# Copyright (C) 2018 Simon Dirmeier
#
# This file is part of pybda.
#
# pybda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pybda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pybda. If not, see <http://www.gnu.org/licenses/>.
#
# @author = 'Simon Dirmeier'
# @email = 'simon.dirmeier@bsse.ethz.ch'


import glob
import logging
import numpy

import pandas
import matplotlib.pyplot as plt
import re

from pybda.fit.clustering_fit_profile import FitProfile
from pybda.globals import K_, LOGLIK_, BIC_

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GMMFitProfile(FitProfile):
    def __init__(self):
        super().__init__()

    def _plot(self, outpath):
        data, labels = self._cluster_sizes(outpath)
        pand = self.as_pandas()
        for suf in ["png", "pdf", "svg", "eps"]:
            self._plot_profile(outpath + "-profile." + suf, pand)
            self._plot_cluster_sizes(
              outpath + "-cluster_sizes-histogram." + suf, data, labels)

    def _cluster_sizes(self, path):
        fls = glob.glob(path + "*/*cluster_sizes.tsv")
        reg = re.compile(".*K(\d+)_cluster_sizes.tsv")
        ll = self.as_pandas()
        logger.info(len(fls))
        frames = [None] * len(fls)
        for i, fl in enumerate(fls):
            t = pandas.read_csv(fl, sep="\t", header=-1, names="c")
            idx = int(reg.match(fl).group(1))
            t[K_] = str(idx).zfill(9)
            frames[i] = [idx, t]
        frames = sorted(frames, key=lambda x: x[0])
        frames = list(filter(lambda x: x[0] in ll["k"].values, frames))
        labels = list(map(lambda x: "K = {}".format(x[0]), frames))
        data = pandas.concat(map(lambda x: x[1], frames))
        return data, labels

    def _plot_profile(self, file_name, profile):
        logger.info("Plotting profile to: {}".format(file_name))
        n = len(profile[K_].values)
        ks = list(map(str, profile[K_].values))
        plt.figure(figsize=(7, 5), dpi=720)
        ax = plt.subplot(211)

        ax.grid(linestyle="")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_ylabel('Negative log-likelihood', fontsize=12)
        cols = ["black"] * n
        cols[numpy.argmax(profile[LOGLIK_].values)] = "#5668AD"
        plt.bar(ks, -profile[LOGLIK_].values, color=cols, alpha=.75, width=0.5)

        ax = plt.subplot(212)
        ax.grid(linestyle="")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel('#components', fontsize=15)
        ax.set_ylabel('BIC', fontsize=12)
        cols = ["black"] * n
        cols[numpy.argmin(profile[BIC_].values)] = "#5668AD"
        plt.bar(ks, profile[BIC_].values, color=cols, alpha=.75, width=0.5)
        plt.savefig(file_name, dpi=720)
