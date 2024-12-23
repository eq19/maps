FROM redis/redis-stack-server:latest

# Copy the last database dump.
COPY dataFile/dump.rdb /data/dump.rdb

CMD ["/entrypoint.sh"]
