#!/usr/bin/env python3
#
# Copyright 2016 Philipp Winter <phw@nymity.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

BIN_WIDTH = 1000

total = 0
skipped = False

print("site,uniqueCount")

with open(sys.argv[1]) as fd:
    for line in fd:

        if not skipped:
            skipped = True
            continue

        line = line.strip()
        line_count, num = line.split(",")
        line_count, num = int(line_count), int(num)

        if num > 0:
            total += 1

        if (line_count % 1000) == 0:
            print("%d,%.3f" % (line_count, float(total) / BIN_WIDTH))
            total = 0
