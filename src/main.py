import sys
import argparse
from parser import CronParser

def main():
	# Use argparse to handle command-line arguments
	parser = argparse.ArgumentParser(
		description="A command-line utility to parse and expand cron expressions into a human-readable table."
	)
	parser.add_argument(
		"input_string",
		type=str,
		help="The cron expression to be parsed. Example: '*/15 0 1,15 * 1-5 /usr/bin/find'"
	)
	args = parser.parse_args() # Parse the provided arguments
	# print(args)

	try:
		cron_parser = CronParser(args.input_string) # Create a CronParser instance
		print(cron_parser.format_output()) # Print the formatted output
	except ValueError as e: # Handle errors and print an appropriate message
		print(f"Error: {str(e)}")
		sys.exit(1) # Exit with an error status

if __name__ == '__main__':
	main()