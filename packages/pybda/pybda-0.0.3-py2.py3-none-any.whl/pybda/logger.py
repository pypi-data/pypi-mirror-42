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

import logging


def set_logger(logfile):
    hdlr = logging.FileHandler(logfile)
    hdlr.setFormatter(formatter())
    root_logger = logging.getLogger()
    root_logger.addHandler(hdlr)


def formatter():
    return logging.Formatter(logger_format())


def logger_format():
    return '[%(asctime)s - %(levelname)s - %(name)s]: %(message)s'

