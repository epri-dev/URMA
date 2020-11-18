
# put the path of your file
#$cd /home/sharif/Dropbox/path_hardness_URMA

echo 'Insert 1 --> all attack paths from internet connected host to a specific target 
      Insert 2 --> all attack paths from a particular host (IP address) to a specific target 
      Insert 3 --> all attack paths from a particular host (state) to a specific target '

read choice

case $choice in
	1 ) python3 Exploit_path_perimeter_host_to_target.py
		;;
	2 ) python3 Exploit_path_IP_to_target.py
	    ;;
	3 ) python3 Exploit_path_state_to_target.py
	    ;;     	
esac


