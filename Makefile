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
	$S/scrape_pitchfx.py 03-23-2008 11-21-2008 $D/pitchfx2008.db 0
	#$S/scrape_pitchfx.py 03-31-2008 03-31-2008 $D/small-test.db 0




# default rules
default: run

clean:
	rm -f $D/test.db
