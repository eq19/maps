FROM redis/redis-stack-server:latest

# Copy the last database dump.
COPY dataFile/dump.rdb /data/dump.rdb
RUN pip install --user ta
RUN pip install --user freqtrade
CMD ["/entrypoint.sh"]
