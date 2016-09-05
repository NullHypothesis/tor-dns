// Copyright 2016 Philipp Winter <phw@nymity.ch>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"path"
	"regexp"
	"strings"
	"time"

	tor "git.torproject.org/user/phw/zoossh.git"
	pcap "github.com/akrennmair/gopcap"
	dns "github.com/miekg/dns"
)

const (
	HEADER_OFFSET       = 42
	MIN_EXITS           = 500
	INTER_REQ_THRESHOLD = time.Second * 60
)

type Statistics struct {
	NumDuplicates uint64
	NumExits      uint64
	NumProcessed  uint64
	NumNotFound   uint64
	NumNotExit    uint64
	NumDNSPkts    uint64
}

var fpr_pattern, _ = regexp.Compile("^[a-f0-9]{40}$")

// Cache consensuses we already parsed.
var cachedCons = make(map[string]*tor.Consensus)

var consensusDir string

func unpack_fpr(name string) string {

	// Domain names are structured as:
	//   FINGERPRINT.RANDOM.tor.nymity.ch.
	labels := strings.Split(name, ".")
	if len(labels) == 0 {
		log.Fatalf("Could not extract labels of %q", name)
	}
	fpr := strings.ToLower(labels[0])

	match := fpr_pattern.MatchString(fpr)
	if !match {
		log.Fatalf("Fingerprint %q does not match", fpr)
	}

	return fpr
}

func loadConsensus(pktTime time.Time) (*tor.Consensus, error) {

	relPath := fmt.Sprintf("%d/consensuses-%d-%02d/%02d/%d-%02d-%02d-%02d-00-00-consensus",
		pktTime.Year(), pktTime.Year(), pktTime.Month(), pktTime.Day(),
		pktTime.Year(), pktTime.Month(), pktTime.Day(), pktTime.Hour())
	file := path.Join(consensusDir, relPath)

	// Check if we already have the consensus cached.
	if consensus, exists := cachedCons[file]; exists {
		return consensus, nil
	}

	consensus, err := tor.ParseConsensusFile(file)
	if err != nil {
		return nil, err
	}
	cachedCons[file] = consensus

	return consensus, nil
}

func getIpAddr(pkt *pcap.Packet) string {

	pkt.Decode()
	if ip, ipOk := pkt.Headers[0].(*pcap.Iphdr); ipOk {
		return net.IP(ip.SrcIp).String()
	}

	return ""
}

func getTotalExitBw(cons *tor.Consensus) (uint64, uint64) {

	var exitBw, numExits uint64

	for _, getRelay := range cons.RouterStatuses {
		relay := getRelay()
		if relay.Flags.Exit {
			exitBw += getRelay().Bandwidth
			numExits++
		}
	}
	return exitBw, numExits
}

func analysePcap(filename string, useHeuristic bool) {

	handle, err := pcap.Openoffline(filename)
	if err != nil {
		log.Fatal(err)
	}

	var cons *tor.Consensus
	var prevTime time.Time
	var totalExitBw uint64
	stats := new(Statistics)
	counter := 0
	req := new(dns.Msg)

	// Keep track of fingerprints we have already seen.  That way, we can
	// discard duplicate DNS requests.
	var observed = make(map[string]bool)

	for pkt := handle.Next(); pkt != nil; counter, pkt = counter+1, handle.Next() {

		// Heuristic to figure out when the first scan stopped and the second
		// one began.  After a certain number of requests, we determine the
		// inter-request delay.  If it starts to exceed our threshold, we
		// assume that the scan ended.
		if useHeuristic {
			if (counter > MIN_EXITS) && (pkt.Time.Sub(prevTime) > INTER_REQ_THRESHOLD) {
				log.Println("Aborting processing because heuristic says we're done.")
				break
			}
		}

		stats.NumDNSPkts++

		// Load the consensus that is the "closest" to the scan in time.
		if cons == nil {
			cons, err = loadConsensus(pkt.Time)
			if err != nil {
				log.Fatal(err)
			}
			totalExitBw, stats.NumExits = getTotalExitBw(cons)
		}

		if err := req.Unpack(pkt.Data[HEADER_OFFSET:]); err != nil {
			log.Fatal(err)
		}

		if len(req.Question) > 1 {
			log.Println("More than one question in DNS message.")
		}
		name := req.Question[0].Name
		fpr := unpack_fpr(name)

		// Ignore duplicates.
		if _, seen := observed[fpr]; seen {
			stats.NumDuplicates++
			continue
		}
		observed[fpr] = true

		relay, found := cons.Get(tor.Fingerprint(fpr))
		if !found {
			stats.NumNotFound++
			continue
		}

		// We are not interested in relays that have a non-empty exit policy,
		// but no exit flag.
		if !relay.Flags.Exit {
			stats.NumNotExit++
			continue
		}

		stats.NumProcessed++
		bwFrac := float64(relay.Bandwidth) / float64(totalExitBw)
		fmt.Printf("%s,%s,%s,%s,%.5f\n", pkt.Time.UTC().Format(time.RFC3339),
			fpr, getIpAddr(pkt), relay.Address, bwFrac)
		prevTime = pkt.Time
	}

	log.Printf("%d DNS packets processed.", stats.NumDNSPkts)
	log.Printf("%d relays not found in consensus.", stats.NumNotFound)
	log.Printf("%d duplicate DNS requests observed.", stats.NumDuplicates)
	log.Printf("%d relays did not have Exit flag.", stats.NumNotExit)
	frac := float64(stats.NumProcessed) / float64(stats.NumExits) * 100
	log.Printf("%d in consensus, %d (%.2f%%) processed.",
		stats.NumExits, stats.NumProcessed, frac)

	if counter < MIN_EXITS {
		log.Fatalf("Only %d DNS requests in pcap.", counter)
	}
}

func main() {

	pcapFile := flag.String("pcap", "", "Pcap file to analyse.")
	consDir := flag.String("consdir", "", "Directory holding consensuses.")
	filterPkts := flag.Bool("filter", false, "Filter packets using heuristic.")
	flag.Parse()

	if *pcapFile == "" {
		log.Fatal("No pcap file given.  Use the -pcap argument.")
	}
	if *consDir == "" {
		log.Fatal("No consensus directory given.  Use the -consdir argument.")
	}
	consensusDir = *consDir

	fmt.Println("time,fingerprint,resolver,relay,bandwidth")
	analysePcap(*pcapFile, *filterPkts)
}
