FROM selaworkshops/alpine_new:3.4
RUN apk add --no-cache python
CMD python -m SimpleHTTPServer 5000