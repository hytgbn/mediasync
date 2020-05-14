


To sync media download folder to server


env variables
* DEST_USER: dest server posix user
* DEST_SERVER: dest server domain/address
* DEST_PATH: path to copy media files to


Note that this deletes files from source.

### Initial configuration


Initial configuration will generate ssh key and upload it to server. You'll be asked to enter password.


```

docker run -it -e DEST_USER=<user> -e DEST_SERVER=<addr> -e DEST_PATH=<path> --mount type=bind,source=<host directory>,target=/mediadir --name mediasync mediasync:latest

```


### Once configured

You can set up a schedule task, e.g. cron, with below command.

```

docker start mediasync

```
