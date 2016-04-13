# -*- coding: utf-8 -*-
# Copyright (C) 2015 Red Hat, Inc.
#
# bugyou_plugins is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# bugyou_plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# bugyou_plugins.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
#

from logging.config import dictConfig

class BaseCommand(object):
    def __init__(self):
        LOGGING_CONF = dict(
            version=1,
            formatters=dict(
                bare={
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "[%(asctime)s][%(name)10s %(levelname)7s] %(message)s"
                },
            ),
            handlers=dict(
                console={
                    "class": "logging.StreamHandler",
                    "formatter": "bare",
                    "level": "DEBUG",
                    "stream": "ext://sys.stdout",
                }
            ),
            loggers=dict(
                bugyou={
                    "level": "DEBUG",
                    "propagate": False,
                    "handlers": ["console"],
                }
            ),
        )
        dictConfig(LOGGING_CONF)
