FROM python:3.7.0-alpine3.8

# TODO remove git from image
RUN apk add --no-cache git

RUN adduser -S ftp-sink
USER ftp-sink
ENV PATH "${PATH}:/home/ftp-sink/.local/bin"

VOLUME /sink
ENV FTP_USERNAME user
ENV FTP_PASSWORD_SHA256 2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b
ENV FTP_CONTROL_PORT 2121
ENV FTP_PASSIVE_PORT 62121
EXPOSE $FTP_CONTROL_PORT $FTP_PASSIVE_PORT

COPY . /pyftpd-sink
RUN pip install --user /pyftpd-sink

# TODO set masquerade address for passive mode
CMD ["pyftpd-sink", "--root-dir", "/sink"]
