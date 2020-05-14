
# Overview

**mediasync** provides a way to upload your media folder to server that runs media servers like Plex, Kodi, etc.

You should have a folder in your host that only contains media files that **mediasync** can read from.

To avoid copying incomplete files, **mediasync** simply checks if the filesize and lastmod date are not changed for 10 seconds.

Note that **mediasync** removes source files after uploading those, with rsync's `--remove-source-files` option.

Any files starting with dot(`.`) will not be transferred and any folders are ignored as well.


# Security

During initial configuration, **mediasync** will generate ssh key and `ssh-copy-id` its public key to server for passwordless rsync operations. You'll be asked to enter password when **mediasync** container copies the public key to the server.

The ssh key will be stored in `/var/keys/` volume.



# Usaage

### Initial configuration

Env variables **mediasync** uses:

* DEST_USER: dest server posix user
* DEST_SERVER: dest server domain/address
* DEST_PATH: path of dest server to copy media files.

```

docker run -it -e DEST_USER=<user> -e DEST_SERVER=<addr> -e DEST_PATH=<path> --mount type=bind,source=<host directory>,target=/mediadir --name mediasync mediasync:latest

#TODO make docker repo public

```


### Periodic upload

You can set up a schedule task, e.g. cron, with below command.

```

docker start mediasync

```

crontab example to check source directory minutely: `* * * * * docker start mediasync`
