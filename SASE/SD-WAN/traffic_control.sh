#!/bin/bash
clear
interface1='eth1'
interface2='eth2'

tc qdisc add dev $interface1 root netem
tc qdisc add dev $interface2 root netem

echo -e "
   Traffic Shaping Emulator script
"

while(true);do

echo -e "
 # Select WAN channel A or B
 A : A channel
 B : B channel
 C : manual test
"

read -p "channel : " channel
clear
if [ $channel == 'A' ];then
   while(true);do
      echo "*A channel selected"
      echo -e "
       c)   Latency 0ms   + Jitter 0%  + 0% Loss (Clear)
       4-1) Latency 80ms  + Jitter 5%  + 1% Loss
       4-2) Latency 80ms  + Jitter 5%  + 3% Loss
       5-1) Latency 200ms + Jitter 5%  + 1% Loss
       5-2) Latency 200ms + Jitter 5%  + 3% Loss
       5-3) Latency 200ms + Jitter 5%  + 5% Loss
       5-4) Latency 200ms + Jitter 10% + 10% Loss
       5-5) Latency 200ms + Jitter 10% + 5% Loss
      "
      read -p "no : " no
      case $no in
      ## latency = ms, jiter_input = %, loss = decimal %
      c )
         latency_input='0'; jitter_input='0'; loss='0%'; echo "ALL Clear selected"; flag='true';;
      4-1 )
         latency_input=40; jitter_input=5; loss='1%'; echo "4-1 selected"; flag='true';;
      4-2 )
         latency_input=40; jitter_input=5; loss='3%'; echo "4-2 selected"; flag='true';;
      5-1 )
         latency_input='100'; jitter_input='5'; loss='1%'; echo "5-1 selected"; flag='true';;
      5-2 )
         latency_input='100'; jitter_input='5'; loss='3%'; echo "5-2 selected"; flag='true';;
      5-3 )
         latency_input='100'; jitter_input='5'; loss='5%'; echo "5-3 selected"; flag='true';;
      5-4 )
         latency_input='100'; jitter_input='10'; loss='10%'; echo "5-4 selected"; flag='true';;
      5-5 )
         latency_input='100'; jitter_input='10'; loss='5%'; echo "5-5 selected"; flag='true';;
      *)
         printf "choose again \n\n"
         sleep 1
      esac
      if [ ! -z $flag ] && [ $flag == 'true' ] ; then
         clear
         jit_cal=$(expr $latency_input \* $jitter_input / 100 )
         jitter=$(echo $jit_cal"ms")
         latency=$(echo $latency_input"ms")
         echo "$no case applied"
         echo "----------------------------------------------------"
         printf "|latency : %6s                                   |\n" $(expr $latency_input \* 2)" ms"
         printf "|jitter :  %6s                                   |\n" $(expr $jit_cal \* 2)" ms"
         printf "|loss :    %6s                                   |\n" $loss
         echo "----------------------------------------------------\n"
         $(tc qdisc change dev $interface1 root netem delay $latency $jitter loss $loss);
         $(tc qdisc change dev $interface2 root netem delay $latency $jitter loss $loss);
         tc qdisc show;
      fi
      echo "------------------------------------------------------"
      done
elif [ $channel == 'B' ]; then
   while(true);do
      echo "*B channel selected"
      echo -e "
       c)   Latency 0ms   + Jitter 0%  + 0% Loss (Clear)
       4-1) Latency 100ms + Jitter 5%  + 1% Loss
       4-2) Latency 100ms + Jitter 5%  + 3% Loss
       5-1) Latency 300ms + Jitter 5%  + 1% Loss
       5-2) Latency 300ms + Jitter 5%  + 3% Loss
       5-3) Latency 300ms + Jitter 5%  + 5% Loss
       5-4) Latency 300ms + Jitter 10% + 10% Loss
       5-5) Latency 300ms + Jitter 10% + 3% Loss
      "
      read -p "no : " no
      case $no in
      ## latency = ms, jiter_input = %, loss = decimal %
      c )
         latency_input='0'; jitter_input='0'; loss='0%'; echo "ALL Clear selected"; flag='true';;
      4-1 )
         latency_input=50; jitter_input=5; loss='1%'; echo "4-1 selected"; flag='true';;
      4-2 )
         latency_input=50; jitter_input=5; loss='3%'; echo "4-2 selected"; flag='true';;
      5-1 )
         latency_input='150'; jitter_input='5'; loss='1%'; echo "5-1 selected"; flag='true';;
      5-2 )
         latency_input='150'; jitter_input='5'; loss='3%'; echo "5-2 selected"; flag='true';;
      5-3 )
         latency_input='150'; jitter_input='5'; loss='5%'; echo "5-3 selected"; flag='true';;
      5-4 )
         latency_input='150'; jitter_input='10'; loss='10%'; echo "5-4 selected"; flag='true';;
      5-5 )
         latency_input='150'; jitter_input='10'; loss='3%'; echo "5-5 selected"; flag='true';;
      *)
         printf "choose again \n\n"
         sleep 1
      esac
      if [ ! -z $flag ] && [ $flag == 'true' ] ; then
         clear
         jit_cal=$(expr $latency_input \* $jitter_input / 100 )
         jitter=$(echo $jit_cal"ms")
         latency=$(echo $latency_input"ms")
         echo "$no case applied"
         echo "----------------------------------------------------"
         printf "|latency : %6s                                   |\n" $(expr $latency_input \* 2)" ms"
         printf "|jitter :  %6s                                   |\n" $(expr $jit_cal \* 2)" ms"
         printf "|loss :    %6s                                   |\n" $loss
         echo "----------------------------------------------------"
         $(tc qdisc change dev $interface1 root netem delay $latency $jitter loss $loss);
         $(tc qdisc change dev $interface2 root netem delay $latency $jitter loss $loss);
         tc qdisc show;
      fi
      echo "----------------------------------------------------"
      done
elif [ $channel == 'C' ]; then
   while(true);do
      echo "## Manual Mode ##"
      read -p "latency : " latency_input
      read -p "jiter : " jitter_input
      read -p "loss : " loss_input
      temp="ms"
      if [ ! -z $latency_input ]; then
         latency=$latency_input$temp; fi
      if [ ! -z $jitter_input ]; then
         jitter=$jitter_input$temp; fi
      if [ ! -z $loss_input ]; then
         loss=$loss_input; fi
      echo "> Manual Settings "
      echo "----------------------------------------------------"
      printf "|latency : %6s                                   |\n" $latency
      printf "|jitter :  %6s                                   |\n" $jitter
      printf "|loss :    %6s                                   |\n" $loss
      echo "----------------------------------------------------"
      $(tc qdisc change dev $interface1 root netem delay $latency $jitter loss $loss);
      $(tc qdisc change dev $interface2 root netem delay $latency $jitter loss $loss);
      tc qdisc show;
      printf "\n\n"
   done

else
  echo "--"

fi

done