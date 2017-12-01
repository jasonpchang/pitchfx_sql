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
	$S/scrape_pitchfx.py 03-31-2008 04-01-2008 $D/small-test.db 0




# default rules
default: run

clean:
	rm -f $D/test.db
