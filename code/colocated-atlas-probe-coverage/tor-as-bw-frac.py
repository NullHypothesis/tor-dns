#!/usr/bin/env python2
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
import pprint

import pyasn
import stem.descriptor.remote

from atlasass import atlas_ass

# The pyasn documentation has instructions on how to generate the following
# lookup file quickly: <https://github.com/hadiasghari/pyasn>
asndb = pyasn.pyasn("ipasn-2016-05-11.dat")

exit_bw = dict()
guard_bw = dict()
total_exit_bw = total_guard_bw = missed_asns = 0

downloader = stem.descriptor.remote.DescriptorDownloader(use_mirrors=True)
for status in downloader.get_consensus():

    asn, _ = asndb.lookup(status.address)
    if asn is None:
        missed_asns += 1
        continue

    if stem.Flag.EXIT in status.flags:
        bw = exit_bw.get(asn, 0)
        exit_bw[asn] = bw + status.bandwidth
        total_exit_bw += status.bandwidth

    if stem.Flag.GUARD in status.flags:
        bw = guard_bw.get(asn, 0)
        guard_bw[asn] = bw + status.bandwidth
        total_guard_bw += status.bandwidth

exit_overlap = set(exit_bw.keys()) & atlas_ass
guard_overlap = set(guard_bw.keys()) & atlas_ass

print("%d out of all %d Tor exit ASs have Atlas probes." %
      (len(exit_overlap), len(exit_bw.keys())))
print("%d out of all %d Tor guard ASs have Atlas probes." %
      (len(guard_overlap), len(guard_bw.keys())))

bw = 0
for asn in exit_overlap:
    bw += exit_bw[asn]
print("Atlas ASs cover %.2f%% of Tor exit ASs." %
      (float(bw) / total_exit_bw * 100))

bw = 0
for asn in guard_overlap:
    bw += guard_bw[asn]
print("Atlas ASs cover %.2f%% of Tor guard ASs." %
      (float(bw) / total_guard_bw * 100))

print("Missed %d relays for which we couldn't look up ASN." % missed_asns)
