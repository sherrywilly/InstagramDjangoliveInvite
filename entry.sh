#!/bin/sh
echo "Now we are in the entrypoint.sh script"
npm install

exec "$@"
