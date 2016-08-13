from create_transaction import create_transaction
from create_category import create_category
from datetime import datetime
import sys
import os

def main():
	hour = datetime.now().time().hour
	greeting = ""
	if hour > 3 and hour < 12:
		greeting = "Good morning!"
	elif hour >= 12 and hour < 6:
		greeting = "Good afternoon!"
	else:
		greeting = "Good evening!"
	options = ["1", "2", "3"]
	while True:
		os.system("clear")
		print(greeting + " What would you like to do?")
		print("1. Create transaction");
		print("2. Create category");
		print("3. Exit");
		
		selected_option = raw_input("Type the option number and hit <Enter>: ")
		while (not selected_option in options):
			os.system("clear")
			print(greeting + " What would you like to do?")
			print("1. Create transaction");
			print("2. Create category");
			print("3. Exit");
			selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

		if (selected_option == options[0]):
			create_transaction()
		elif (selected_option == options[1]):
			create_category()
		elif (selected_option == options[2]):
			os.system("clear")
			sys.exit("See you later!")
		else:
			sys.exit("Error")

if __name__ ==  "__main__":
	main()
