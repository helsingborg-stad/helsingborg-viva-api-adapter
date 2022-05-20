#!/bin/bash

ssh -S viva-ctrl-socket -O exit hbgintra@intranat.helsingborg.se
echo 'Viva tunnel closed'

exit 0
