FROM freqtradeorg/freqtrade:develop

# Switch user to root if you must install something from apt
# Don't forget to switch the user back below!
# USER root

# The below dependency - pyti - serves as an example. Please use whatever you need!
ADD dataFile/user_data /home/runner/user_data
WORKDIR /home/runner/user_data
RUN build_helpers/install_ta-lib.sh

# Switch back to user (only if you required root above)
USER ftuser
RUN pip install --user ta
