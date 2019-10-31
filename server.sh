#!/bin/bash

# echo Enter callsign:
read callsign

python3 client.py $callsign

clear

echo Press CTRL+D to close connection...
