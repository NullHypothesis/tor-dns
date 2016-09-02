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

import stem.exit_policy
import stem.descriptor.remote

def main():

    reduced_policy = stem.exit_policy.ExitPolicy("accept *:20-21, accept *:22, accept *:23, accept *:43, accept *:53, accept *:79, accept *:80-81, accept *:88, accept *:110, accept *:143, accept *:194, accept *:220, accept *:389, accept *:443, accept *:464, accept *:465, accept *:531, accept *:543-544, accept *:554, accept *:563, accept *:587, accept *:636, accept *:706, accept *:749, accept *:873, accept *:902-904, accept *:981, accept *:989-990, accept *:991, accept *:992, accept *:993, accept *:994, accept *:995, accept *:1194, accept *:1220, accept *:1293, accept *:1500, accept *:1533, accept *:1677, accept *:1723, accept *:1755, accept *:1863, accept *:2082, accept *:2083, accept *:2086-2087, accept *:2095-2096, accept *:2102-2104, accept *:3128, accept *:3389, accept *:3690, accept *:4321, accept *:4643, accept *:5050, accept *:5190, accept *:5222-5223, accept *:5228, accept *:5900, accept *:6660-6669, accept *:6679, accept *:6697, accept *:8000, accept *:8008, accept *:8074, accept *:8080, accept *:8082, accept *:8087-8088, accept *:8332-8333, accept *:8443, accept *:8888, accept *:9418, accept *:9999, accept *:10000, accept *:11371, accept *:19294, accept *:19638, accept *:50002, accept *:64738, reject *:*")
    web_policy = stem.exit_policy.ExitPolicy("accept *:80, accept *:443")

    num_reduced = num_web = num_exits = 0
    total_bw = reduced_bw = web_bw = 0

    for desc in stem.descriptor.remote.get_server_descriptors():

        # We are only interested in exit relays.

        if not desc.exit_policy.is_exiting_allowed():
            continue

        num_exits += 1
        total_bw += desc.observed_bandwidth
        print(desc.exit_policy.summary())

        if desc.exit_policy.summary() == reduced_policy.summary():
            num_reduced += 1
            reduced_bw += desc.observed_bandwidth
        elif desc.exit_policy.summary() == web_policy.summary():
            num_web += 1
            web_bw += desc.observed_bandwidth


    print("Among all %d exit relays, %d (%.2f%%) have reduced and %d "
          "(%.2f%%) have web policy." %
          (num_exits, num_reduced, float(num_reduced) / num_exits * 100,
           num_web, float(num_web) / num_exits * 100))

    print("Reduced policy accounts for %.2f%% and web policy accounts for "
          "%.2f%% of exit bandwidth." %
          (float(reduced_bw) / total_bw * 100,
           float(web_bw) / total_bw * 100))

if __name__ == "__main__":
    sys.exit(main())
