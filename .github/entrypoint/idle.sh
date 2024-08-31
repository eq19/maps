#!/usr/bin/env bash

# Run script on system idle https://askubuntu.com/a/506975/486942
while sleep 30s ; do
   state=$(gnome-screensaver-command --query | grep -o "\w*active\w*" >> /dev/null)
   if [[ $state == active ]]
   then
        ./start.sh
   else
        ./stop.sh
   fi
done