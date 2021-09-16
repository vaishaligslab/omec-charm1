#!/bin/bash
a=$1
echo "This script is about to run another script."
sh /bin/a.sh $a
#sh /home/vagrant/shellcode/123/b.sh
echo "This script has just run another script."

