# A simple interface for APDU testing
# By Brandon Hammond

# Import required modules
import os
import sys
from ledgerblue.comm import getDongle

# Define the main() function
def main():
	# Function: main()
	# Purpose: Act as an interface for testing APDU commands

	# Get the dongle
	dongle = getDongle(True)

	# Create an infinite loop for sending user specified APDU commands
	while True:
		# Get the APDU command from the user
		command = raw_input("=>")

		# Transfer the APDU command to the dongle
		dongle.exchange(bytes(command.decode("hex")))

		# Note that the response will be displayed by
		# the dongle.exchange() function rather than
		# by this script. It is an odd design, but
		# it works. 

# Make sure not running as a module and call main()
if __name__ == "__main__":
	main()
