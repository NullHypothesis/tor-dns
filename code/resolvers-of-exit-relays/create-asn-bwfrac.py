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

import io
import os
import sys
import csv
import pyasn
import operator
import logging as log
import subprocess

# Object that maps IP addresses to AS numbers.

asndb = None

# Maps timestamps to ASNs.

output = dict()

# Pseudo ASN that signals local resolvers.

LOCAL = 0

# The amount of top ASs we are interested in.

TOP_N = 3

# The minimum number of DNS requests we expect in a file.

MIN_REQUESTS = 500

# Set of ASs that were ever in the top five of any file.

top_ass = set()

# Set of ASs that were ever in the top five of any file.  If this set
# disagrees with `top_ass' that is determined at runtime, we will have to
# update this list.

ASNS = frozenset([0, 15169, 13030, 60781, 9008,
                  16276, 36692, 43350, 37560, 3356])


def process_output(csvstring):
    """
    Process the output of our analysis tool.

    The output is of the form:

      time, fingerprint, resolver_addr, relay_addr, bw_fraction

    We map the resolver's IP address to its ASN and store its cumulative
    bandwidth fraction.  The final output allows us to determine how much DNS
    bandwidth each AS controls.
    """

    asnbw = dict()
    ref_time = None
    skipped_header = False
    total_bw = 0

    # Each line is a DNS request for one exit relay.

    for line in io.StringIO(csvstring.decode("unicode_escape")):

        if not skipped_header:
            skipped_header = True
            continue

        time, fpr, resolver, relay, bw = [x.strip() for x in line.split(",")]

        # Take the first timestamp and use it in the final output.

        if ref_time is None:
            ref_time = time

        # Local or third-party DNS resolver?

        if resolver == relay:
            asn = LOCAL
        else:
            asn, _ = asndb.lookup(resolver)
            if asn is None:
                log.info("Could not resolve ASN for %s", resolver)
                continue

        total_bw += float(bw)
        asnbw[asn] = asnbw.get(asn, 0) + float(bw)

    if ref_time is None:
        log.warning("ref_time is none.")
        return

    # Get top n ASs by bandwidth and keep track of them.

    top_n = sorted(asnbw.items(),
                   key=operator.itemgetter(1),
                   reverse=True)[:TOP_N]

    for asn, bw in top_n:
        top_ass.add(asn)

    output[ref_time] = dict()
    for asn in ASNS:
        output[ref_time][asn] = asnbw.get(asn, 0)


def create_output():
    """
    Write CSV-formatted output to stdout.
    """

    # Output is a CSV of the form:
    #
    #   time, ASN1, ASN2, ASN3, ...
    #   t_0,     0,   13,   14,
    #   t_1,     5,   15,   11,
    #   t_2,     7,   18,    0,
    #   ...

    print("time,", end="")
    for asn in sorted(ASNS):
        print("as%d," % asn, end="")
    print("total")

    # Print output, lexically sorted by date.

    for time, asnbw in sorted(output.items()):

        print(time + ",", end="")

        for asn in ASNS:
            asnbw.setdefault(asn, 0)

        for _, bw in sorted(asnbw.items()):
            print("%.5f," % bw, end="")
        print("%.5f" % sum(asnbw.values()))


def process_files(dirname, cons_dir):
    """
    Find files and run analysis tools over them.
    """

    # Get list of files to process.

    if os.path.isfile(dirname):
        files = [dirname]
    else:
        files = os.listdir(dirname)
        files = [os.path.join(dirname, f) for f in files]
        files.sort()

    # Process each pcap file.

    for f in files:
        if not f.endswith(".pcap"):
            continue
        log.info("Processing file: %s" % f)

        cmd = ["./analyse-pcap", "-pcap", f, "-consdir", cons_dir]
        try:
            csvstring = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            log.warning("Non-zero exit code for %s" % f)
            continue

        num_reqs = len(csvstring.decode("unicode_escape").split("\n"))
        if num_reqs < MIN_REQUESTS:
            log.warning("Only %d requests in output.  Skipping.", num_reqs)
            continue

        process_output(csvstring)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: %s PCAP_DIR CONSENSUS_DIR ASNDB" %
              sys.argv[0], file=sys.stderr)
        sys.exit(1)

    asndb = pyasn.pyasn(sys.argv[3])
    process_files(sys.argv[1], sys.argv[2])
    create_output()

    if top_ass != ASNS:
        log.critical("Top ASs not the same as hard-coded ASs.  "
                     "Update with: %s", top_ass)

    sys.exit(0)
