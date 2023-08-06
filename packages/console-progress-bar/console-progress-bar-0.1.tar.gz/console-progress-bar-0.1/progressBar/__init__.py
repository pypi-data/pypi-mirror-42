# -*- coding: utf-8 -*-
import datetime
import sys


def _timedelta2str(timedelta):
    return str(timedelta).split(".")[0]


def _overwrite_current_line(output):
    sys.stdout.write('\r')
    sys.stdout.write(output)
    sys.stdout.flush()


class ProcessBar():

    def __init__(self, total, bar_length=30):
        assert (type(total)) == int, "Please enter a int as total number."
        self.total = total
        self.bar_length = bar_length
        self.__begin = datetime.datetime.now()
        self.count = 1

        self.__print_title()

    def __create_title(self):
        title_bar = "{:^{bar_length}}".format("bar", bar_length=self.bar_length)
        progress_width = len(str(self.total)) * 2 + 7
        title_progress = "{:^{width}}".format("progress", width=progress_width)
        title_cost = "{:^8}".format("cost")
        title_remain = "{:^8}".format("remain")
        title_current = "current"
        return "|".join([title_bar, title_progress, title_cost, title_remain, title_current])

    def __print_title(self):
        title = self.__create_title()
        print(title)

    def __calculate_time(self):
        now = datetime.datetime.now()
        time_cost = now - self.__begin
        time_remain = time_cost / self.count * (self.total - self.count)
        return time_cost, time_remain

    def __format_update_msg(self, percent, time_cost, time_remain, msg):
        str_progress = "{:>4.0%}({:>{width}}/{})".format(percent, self.count, self.total, width=len(str(self.total)))
        str_time_cost = "{:>8}".format(_timedelta2str(time_cost))

        if percent > 1:
            str_time_remain = "EXPLODED"
            str_bar = "{:<{BAR_LENGTH}}".format(self.bar_length * "█", BAR_LENGTH=self.bar_length)
        else:
            str_time_remain = "{:>8}".format(_timedelta2str(time_remain))
            str_bar = "{:<{BAR_LENGTH}}".format(int(percent * self.bar_length) * "█", BAR_LENGTH=self.bar_length)
        return "|".join([str_bar, str_progress, str_time_cost, str_time_remain, msg])

    def update(self, msg=""):
        time_cost, time_remain = self.__calculate_time()
        percentage = float(self.count / self.total)
        output = self.__format_update_msg(percentage, time_cost, time_remain, msg)
        _overwrite_current_line(output)
        self.count += 1


