#!/bin/bash

# Check if /etc/os-release exists
if [ -f /etc/os-release ]; then
    # Load system information from /etc/os-release
    . /etc/os-release
    # Check if the OS is Ubuntu and if the version ID starts with '20'
    if [ "$ID" = "ubuntu" ] && [[ "$VERSION_ID" =~ ^20 ]]; then
         echo "$PRETTY_NAME"
	     pip3 install together
    	 pip3 install nltk
    	 pip3 install pandas
         python3 -m nltk.downloader punkt punkt_tab wordnet
	 exit 0
    fi
fi

echo "This script has been tested on ubuntu20, may not be suitable for your system version."


# Prompt the user for confirmation
read -p "This script can force execute the install command on others system. Do you want to continue? (Y/y to proceed): " answer

# Check if the answer is 'Y' or 'y'
if [[ "$answer" == "Y" || "$answer" == "y" ]]; then
    echo "Proceeding with the command execution..."
    pip3 install together
    pip3 install nltk
    pip3 install pandas
    python3 -m nltk.downloader punkt punkt_tab wordnet
    
else
    echo "Execution cancelled."
    exit 1
fi

