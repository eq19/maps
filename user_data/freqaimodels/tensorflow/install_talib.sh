# curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz -O && tar xzvf ta-lib-0.4.0-src.tar.gz
# cd ta-lib && ./configure --prefix=/usr && make && make install && cd .. && pip install ta-lib && rm -rf ta-lib-0.4.0-src.tar.gz ta-lib/

# cd /tmp && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar xf ta-lib-0.4.0-src.tar.gz \
    # && cd ta-lib && ./configure --prefix=${VIRTUAL_ENV:-/usr} && make -j$(nproc) && make -j$(nproc) install && pip install ta-lib \
    # && cd .. && rm -rf ta-lib-0.4.0-src.tar.gz ta-lib

cd /tmp && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar xf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib && ./configure --prefix=/notebooks/.usr && make install && pip install ta-lib \
    && cd .. && rm -rf ta-lib-0.4.0-src.tar.gz ta-lib
