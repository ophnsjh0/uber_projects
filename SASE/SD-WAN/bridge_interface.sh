#!/bin/bash
read -p "1st interface to bridge : " int1
read -p "2nd interface to bridge : " int2
ifconfig $int1 0.0.0.0 up
ifconfig $int2 0.0.0.0 up
sleep 0.5
brctl addbr br0
echo "Making bridge.."
sleep 0.5
brctl addif br0 $int1
echo "adding $int1 to bridge br0.."
sleep 0.5
brctl addif br0 $int2
echo "adding $int2 to bridge br0.."
sleep 0.5
ifconfig br0 192.168.128.69 netmask 255.255.255.0
sleep 0.5
brctl show
echo "---------------------------"
echo "Initialization complete!"
echo "---------------------------"