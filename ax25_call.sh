#!/bin/bash

# Bash script to serve as a wrapper for "ax25_call" and allow for standard 
# LF to be sent from a Linux environment and display and appear like in a 
# traditional shell like "telnet" or "nc"
#
# Usage:
#   ./ax25_call.sh ax25_portname local_callsign remote_callsign
#
# Evan Chodora (AF5E), 2019
# https://github.com/evanchodora/~

# Check to ensure ax25_call is available
if ! [ -x "$(command -v ax25_call)" ]; then
        echo 'Error: ax25_apps and/or ax25_tools is missing'
        exit 1
fi

# Script usage help line
usage() { 
echo "Wrapper for \"ax25_call\" that replicates normal shells"
echo "Usage: $0 port local_call remote_call [-h | --help]"
echo "See \"man ax25_call\" for more information." 1>&2; }

# Check for proper flags for help
while getopts ":h" o; do
	case "${o}" in
		h)
			usage
			exit 0
			;;
		*)
			usage
			exit 1
			;;
	esac
done
shift $((OPTIND-1))

# Check if three arguments were passed to the script
if [ $# -lt 3 ]; then
        echo "Missing required port and callsign parameters"
        echo "$0 --help for more information"
        exit 1
fi

# Store variables
port=$1
local_call=$2
remote_call=$3

# Run ax25_call with improved conversion between LF and CR
stdbuf -i0 -o0 unix2dos -c mac | \
        ax25_call $port $local_call $remote_call | \
        stdbuf -i0 -o0 dos2unix -c mac

