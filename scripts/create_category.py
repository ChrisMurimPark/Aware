import mysql.connector
from mysql.connector import errorcode
import sys
import os

def create_category():
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


	os.system("clear")
	new_category = raw_input("New category name: ")
	while (new_category == "" or len(new_category) > 30):
		os.system("clear")
		if new_category == "":	
			print("Sorry, it can't be blank.")
		else:
			print("Sorry, that name is too long.")
		new_category = raw_input("New category name: ")

	# at this point, we have connected to the database
	cursor = cnx.cursor()

	add_category = ("INSERT INTO categories " 
					"(name) " 
					"VALUES (%(name)s)")
	category_data = { 'name': new_category }
	cursor.execute(add_category, category_data)

	cnx.commit()

	cursor.close()
	cnx.close()

	options = ["1", "2"]
	os.system("clear")
	print("Success! New category:\n")
	print("\t" + new_category)
	print("\n1. Back to Main Menu")
	print("2. Exit")
	selected_option = raw_input("Type the option number and hit <Enter>: ")
	while (not selected_option in options):
		os.system("clear")
		print("Success! New category:\n")
		print("\t" + new_category)
		print("\n1. Back to Main Menu")
		print("2. Exit")
		selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

	if (selected_option == options[1]):
		os.system("clear")
		sys.exit("See you later!")
