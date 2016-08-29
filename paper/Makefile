TARGET=paper
all: pdf

replication:
	GS_OPTIONS=-dPDFSETTINGS=/prepress rubber -f --pdf -Wrefs -Wmisc replication

pdf:
	GS_OPTIONS=-dPDFSETTINGS=/prepress rubber -f --pdf -Wrefs -Wmisc $(TARGET)
	GS_OPTIONS=-dPDFSETTINGS=/prepress rubber -f --pdf -Wrefs -Wmisc $(TARGET)-alt

alt:
	GS_OPTIONS=-dPDFSETTINGS=/prepress rubber -f --pdf -Wrefs -Wmisc $(TARGET)-alt

clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.brf *~ *.bak $(TARGET).pdf $(TARGET).ps *.toc *.lot *.lof *.bcf *.run.xml $(TARGET)-alt.pdf $(TARGET)-alt.ps

cleanall: clean
	rm -f $(TARGET).pdf $(TARGET)-alt.pdf

ps: pdf
	GS_OPTIONS=-dPDFSETTINGS=/prepress pdftops -level1 $(TARGET).pdf
	GS_OPTIONS=-dPDFSETTINGS=/prepress pdftops -level1 $(TARGET)-alt.pdf
