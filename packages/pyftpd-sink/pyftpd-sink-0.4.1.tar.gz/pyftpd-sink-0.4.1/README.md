# pyftpd-sink

`pyftpd-sink --help`

## docker 🐳

docker hub: https://hub.docker.com/r/fphammerle/pyftpd-sink/

```sh
sudo docker run --rm \
    -v /tmp/ftp-sink:/sink \
    -e FTP_USERNAME=user \
    -e FTP_PASSWORD_SHA256=2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b \
    -p 2121:2121 -p 62121:62121 \
    --security-opt=no-new-privileges --cap-drop=all \
    fphammerle/pyftpd-sink
```
