#!/bin/bash

ssh -M -S viva-ctrl-socket -fnNT -L 8080:a002527.hbgadm.hbgstad.se:80 hbgintra@intranat.helsingborg.se
echo 'Viva (a002527) tunnel established'

exit 0
