#####################################################
# Makefile for running code
#   - parses information
#####################################################

# definitions
S = ./src
D = ./Dat

# keep intermediate files
.SECONDARY: 


# run code
run:
	$S/scrape_pitchfx.py 03-31-2009 10-01-2009 $D/pitchfx2008-2009.db 0




# default rules
default: run

clean:
	rm -f $D/test.db
