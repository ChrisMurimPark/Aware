import mysql.connector
import sys
import os
from show_categories import show_categories

def delete_category(show_fail, skip_init):
	# show categories with IDs
	show_categories(True)
	
	options = ["1", "2"]
	if show_fail:
		print("\nSorry, that delete didn't work.")
		print("1. Try again")
		print("2. Back to main menu")
	else:
		print("\n1. Delete by ID")
		print("2. Back to main menu")
	selected_option = ""
	if skip_init:
		selected_option = options[0]
	else:
		selected_option = raw_input("Type the option number and hit <Enter>: ")
	while selected_option not in options:
		os.system("clear")
		show_categories(True)
		if show_fail:
			print("\nSorry, that delete didn't work.")
			print("1. Try again")
			print("2. Back to main menu")
		else:
			print("\n1. Delete by ID")
			print("2. Back to main menu")
		selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

	if selected_option == options[0]:
		os.system("clear")
		show_categories(True)
		print("\nWhich category would you like to delete?")
		id_to_delete = raw_input("Type the category ID and hit <Enter>: ")

		# make sure database can be connected to
		try:
			cnx = mysql.connector.connect(user='root', password='abc123', host='localhost', database='cost_analysis')
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with your username or password")
				sys.exit()
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
				sys.exit()
			else:
				print(err)
				sys.exit()

		# at this point, we have connected to the database
		cursor = cnx.cursor()
		delete_query = "DELETE FROM categories WHERE id = " + id_to_delete.strip()
		cursor.execute(delete_query)

		if cursor.rowcount == 0:
			delete_category(True, False)
		else:
			cnx.commit()
			cursor.close()
			cnx.close()

			post_delete_options = ["1", "2"]
			os.system("clear")
			show_categories(True)

			print("\n1. Delete another")
			print("2. Back to main menu")

			post_delete_selected_option = raw_input("Type the option number and hit <Enter>: ")
			while post_delete_selected_option not in post_delete_options:
				os.system("clear")
				show_categories(True)
				print("\n1. Delete another")
				print("2. Back to main menu")
				post_delete_selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

			if post_delete_selected_option == post_delete_options[0]:
				delete_category(False, True)

