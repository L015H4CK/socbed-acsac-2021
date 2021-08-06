# Copyright 2016, 2017, 2018, 2019 Fraunhofer FKIE
#
# This file is part of BREACH.
#
# BREACH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BREACH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BREACH. If not, see <http://www.gnu.org/licenses/>.


class Printer:
    def print(self, msg):
        pass


class ConsolePrinter(Printer):
    def print(self, msg):
        super().print(msg=msg)
        print(msg)


class FilePrinter(Printer):
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.file = file

    def print(self, msg):
        super().print(msg=msg)
        with open(self.file, "a+") as f:
            print(msg, file=f)


class ListPrinter(Printer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.printed = list()

    def print(self, msg):
        super().print(msg=msg)
        self.printed.append(msg)


class MultiPrinter(Printer):
    def __init__(self, printers, **kwargs):
        super().__init__(**kwargs)
        self.printers = printers

    def print(self, msg):
        super().print(msg=msg)
        for printer in self.printers:
            printer.print(msg=msg)
