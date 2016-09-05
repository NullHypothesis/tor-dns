Visualising fraction of DNS requests that ASs can see
-----------------------------------------------------

These instructions tell you how you can turn a set of pcap files containing
DNS queries (that were generated using the
[exitmap](https://github.com/NullHypothesis/exitmap) module dnsenum.py) into a diagram
illustrating the fraction of DNS requests that powerful ASs can see over time.

First, build the Go analysis tool:

    go build analyse-pcap.go

You will also need an archive of consensus files which you can get from
[CollecTor](https://collector.torproject.org).  You only need consensuses for
the time span that is covered in your pcap files.  Make sure to mirror
CollecTor's directory structure.  That is, the consensus directory should have
the following format:

    consensuses/2016/consensuses-2016-04/01/2016-04-01-00-00-00-consensus

The [pyasn](https://github.com/hadiasghari/pyasn) project has instructions on
how to create an IP-to-ASN mapping database.  It doesn't take long.  Now, we
can use the Python tool to analyse all pcap files and, using an archive of our
consensuses and our IP-to-ASN mapping database, create a CSV file that holds
the bandwidth fraction of the top ASs:

    ./create-asn-bwfrac.py /path/to/pcap/dir/ /path/to/consensuses/ /path/to/ipasndb > asn-bw-frac.csv

Finally, use the provided R script to turn the CSV file into a diagram:

    Rscript plot-resolvers-of-exits.R asn-bw-frac.csv

Have a look at the new plot, written to asn-bw-frac.pdf.

The file dnsenum.py is an exitmap module that you can use to create your own
dataset.  To make it available, just copy it to
`path/to/exitmap/src/modules/dnsenum.py` However, that also requires running
your own DNS server.
