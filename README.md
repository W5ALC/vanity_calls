# vanity_calls

this script pulls the current amateur radio callsign data from the FCC, extracts the zip file amd displays the 1x2 or 2x1 callsigns that are currently or soon to be available.

find a callsign you like and look up at https://www.radioqth.net/vanity/available to see when its available.

## Run the script

`python3 <(curl -s https://raw.githubusercontent.com/W5ALC/vanity_calls/master/find_calls.py)`

Run the script and it will print the remaining options for 1x2 and 2x1 calls in the US.  If you want to see regions 11-13 as well  (Alaska, Caribbean, Hawaii), call two_by_one() with False instead of True.
