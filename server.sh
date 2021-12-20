#!/bin/bash
ssh -M -S viva-ctrl-socket -fnNT -L 8080:a002527.hbgadm.hbgstad.se:80 hbgintra@intranat.helsingborg.se
echo 'Tunnel established'

echo 'VADA Development Server'
pipenv run flask run

ssh -S viva-ctrl-socket -O exit hbgintra@intranat.helsingborg.se
echo 'Tunnel closed'
