#!/bin/bash

function pause() {
  read -p "$*"
}

ssh -M -S vader-tunnel-ctrl-socket -fnNT -R 5000:localhost:5000 vader@tunnel.api.helsingborg.io
echo 'Vada localhost vader tunnel established'

pause 'Press [Enter] key to close the vader tunnel...'

ssh -S vader-tunnel-ctrl-socket -O exit vader@tunnel.api.helsingborg.io
echo 'Vader tunnel closed. Bye!'
