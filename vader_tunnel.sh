#!/bin/bash

function pause() {
  read -p "$*"
}

ssh -M -S vader-tunnel-ctrl-socket -fnNT -R 5000:127.0.0.1:5000 vader@tunnel.api.helsingborg.io
echo 'Vada localhost vader-tunnel established.'

pause 'Press [Enter] to close the tunnel...'

ssh -S vader-tunnel-ctrl-socket -O exit vader@tunnel.api.helsingborg.io
echo 'Vader-tunnel closed. Bye! :)'
