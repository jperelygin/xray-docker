FROM teddysun/xray:latest

RUN apk add --no-cache inotify-tools

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD [ "/entrypoint.sh" ]