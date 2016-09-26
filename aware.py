from create_transaction import create_transaction
from create_category import create_category
from show_transactions import delegate_show_transactions
from delete_transaction import delete_transaction
from show_categories import delegate_show_categories
from delete_category import delete_category
from analysis import show_analysis
from datetime import datetime
import sys
import os

def main():
	hour = datetime.now().time().hour
	greeting = ""
	if hour > 3 and hour < 12:
		greeting = "Good morning!"
	elif hour >= 12 and hour < 18:
		greeting = "Good afternoon!"
	else:
		greeting = "Good evening!"
	options = ["1", "2", "3", "4", "5", "6", "7", "8"]
	while True:
		os.system("clear")
		print(greeting + " What would you like to do?")
		print("1. Create transaction")
		print("2. Show transactions")
		print("3. Delete transaction")
		print("4. Create category")
		print("5. Show categories")
		print("6. Delete category")
		print("7. Analyze")
		print("8. Exit")
		
		selected_option = raw_input("Type the option number and hit <Enter>: ")
		while (not selected_option in options):
			os.system("clear")
			print(greeting + " What would you like to do?")
			print("1. Create transaction")
			print("2. Show transactions")
			print("3. Delete transaction")
			print("4. Create category")
			print("5. Show categories")
			print("6. Delete category")
			print("7. Analyze")
			print("8. Exit")
			selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

		if (selected_option == options[0]):
			create_transaction()
		elif (selected_option == options[1]):
			delegate_show_transactions("date", True)
		elif (selected_option == options[2]):
			delete_transaction(False, False)		
		elif (selected_option == options[3]):
			create_category()
		elif (selected_option == options[4]):
			delegate_show_categories()
		elif (selected_option == options[5]):
			delete_category(False, False)
		elif (selected_option == options[6]):
			show_analysis()
		elif(selected_option == options[7]):
			os.system("clear")
			sys.exit("See you later!")
		else:
			sys.exit("Error")

if __name__ ==  "__main__":
	main()
