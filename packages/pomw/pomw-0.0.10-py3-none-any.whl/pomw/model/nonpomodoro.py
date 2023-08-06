# -*- python-indent-offset: 4; -*-

from datetime import datetime

from .interval import Interval


class NonPomodoro(Interval):
    def __init__(self, start_time=None, end_time=None):
        super().__init__(start_time=start_time, end_time=end_time)

    @staticmethod
    def __json_decode__(d):
        return NonPomodoro(
            start_time=d.get("_Interval__start_time", None),
            end_time=d.get("_Interval__end_time", None),
        )
