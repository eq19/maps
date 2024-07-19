#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

export RED=$(tput setaf 1 :-"" 2>/dev/null)
export GREEN=$(tput setaf 2 :-"" 2>/dev/null)
export YELLOW=$(tput setaf 3 :-"" 2>/dev/null)
export BLUE=$(tput setaf 4 :-"" 2>/dev/null)
export RESET=$(tput sgr0 :-"" 2>/dev/null)

echo $GREEN some text $RESET
echo $RED; printf -- "-%.0s" $(seq $(tput cols)); echo $RESET
echo $YELLOW more text $RESET

echo -e "\n$hr\nIdentity\n$hr"
whoami
pwd
id

echo -e "\n$hr\nService Status\n$hr"
service --status-all

echo -e "\n$hr\nSupervisor\n$hr"
apt-cache show supervisor

echo -e "\n$hr\nLocate Initdb\n$hr"
locate initdb

echo -e "\n$hr\DB Cluster\n$hr"
/etc/init.d/postgresql restart
