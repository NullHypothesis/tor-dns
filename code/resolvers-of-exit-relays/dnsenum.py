# Copyright 2015-2016 Philipp Winter <phw@nymity.ch>
#
# This file is part of exitmap.
#
# exitmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# exitmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with exitmap.  If not, see <http://www.gnu.org/licenses/>.
"""
Module to determine an exit relay's DNS server.
"""

import sys
import time
import socket
import logging

import util
import torsocks
import error

log = logging.getLogger(__name__)

destinations = None

# Make sure to configure a domain whose DNS server you control.

TARGET_DOMAIN = ""


def resolve(exit_desc):
    """
    Resolve exit relay-specific domain.
    """

    exit_url = util.exiturl(exit_desc.fingerprint)

    # Prepend the exit relay's fingerprint so we know which relay issued the
    # DNS request.

    fingerprint = exit_desc.fingerprint.encode("ascii", "ignore")
    domain = "%s.%s.%s" % (fingerprint,
                           time.strftime("%Y-%m-%d-%H"),
                           TARGET_DOMAIN)

    log.debug("Resolving %s over %s." % (domain, exit_url))

    sock = torsocks.torsocket()
    sock.settimeout(10)

    # Resolve the domain using Tor's SOCKS extension.

    log.debug("Resolving %s over %s." % (domain, exit_url))
    try:
        ipv4 = sock.resolve(domain)
    except error.SOCKSv5Error as err:

        # This is expected because all domains resolve to 127.0.0.1.

        log.warning("SOCKSv5 error while resolving domain: %s" % err)
        ipv4 = "0.0.0.0"
        pass
    except socket.timeout as err:
        log.debug("Socket over exit relay %s timed out: %s" % (exit_url, err))
        return

    log.info("Successfully resolved domain over %s to %s." % (exit_url, ipv4))

    # Log a CSV including timestamp, exit fingerprint, exit IP address, and the
    # domain we resolved.

    timestamp = time.strftime("%Y-%m-%d_%H:%M:%S_%z")
    content = "%s, %s, %s, %s\n" % (timestamp,
                                    fingerprint,
                                    exit_desc.address,
                                    ipv4)
    util.dump_to_file(content, fingerprint)


def probe(exit_desc, run_python_over_tor, run_cmd_over_tor, **kwargs):
    """
    Make the given exit relay resolve a domain under our control.
    """

    if not len(TARGET_DOMAIN):
        log.critical("Initialise the variable TARGET_DOMAIN.")
        sys.exit(1)

    run_python_over_tor(resolve, exit_desc)
