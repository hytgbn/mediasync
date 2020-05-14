#!/bin/bash
set -eux

# DEST_USER
# DEST_SERVER
# DEST_PATH

KEYS_DIR="/var/keys"


if [ -z "$DEST_USER" ]; then
  echo "DEST_USER variable should be set."
  exit 1
fi
if [ -z "$DEST_SERVER" ]; then
  echo "DEST_USER variable should be set."
  exit 1
fi
if [ -z "$DEST_PATH" ]; then
  echo "DEST_USER variable should be set."
  exit 1
fi

sshkey="$KEYS_DIR/id_rsa"
pubkey="$sshkey.pub"

if [ ! -f $sshkey ]; then
    echo "no key file found for $DEST_USER@$DEST_SERVER. creating one."

    ssh-keygen -t rsa -N "" -f $sshkey
    sed -i "s/root@/$DEST_USER@/" $pubkey
    chmod 400 $sshkey
    ssh-copy-id -o StrictHostKeyChecking=no -i $pubkey $DEST_USER@$DEST_SERVER
fi

/usr/bin/python3.7 /usr/src/app/sync.py --sshkey "$sshkey" --server "$DEST_SERVER" --user "$DEST_USER" --path "$DEST_PATH"
