from prettytable import PrettyTable
import mysql.connector
import sys
import os

def delegate_show_categories():
	show_categories(False)
	show_categories_options()

def show_categories(show_id):
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

	get_categories = "SELECT * FROM categories ORDER BY name"
	cursor.execute(get_categories)
	categories_query_results = cursor.fetchall()

	pretty_table = PrettyTable()
	if show_id:
		pretty_table.field_names = ['ID', 'Category']
	else:
		pretty_table.field_names = ['Category']

	os.system("clear")
	if len(categories_query_results) == 0:
		print "There's nothing here! Use the main menu to add a category."
	else:
		for category in categories_query_results:
			if show_id:
				pretty_table.add_row([category[1], category[0]])
			else:
				pretty_table.add_row([category[0]])
	print(pretty_table)
	# close stuff
	cursor.close()
	cnx.close()

def show_categories_options():
	post_show_options = ["1", "2"]
	print("\n1. Back to main menu")
	print("2. Exit")
	selected_final_option = raw_input("Type the option number and hit <Enter>: ")
	while selected_final_option not in post_show_options:
		os.system("clear")
		if len(transaction_query_results) == 0:
			print "There's nothing here! Use the main menu to add a category."
		else:
			for row in pretty_rows:
				print table_divider
				print row
			print table_divider
		print("\n1. Back to main menu")
		print("2. Exit")
		selected_final_option = raw_input("Sorry, that's not a valid option. Try again: ")
	if selected_final_option == post_show_options[1]:
		os.system("clear")
		sys.exit("See you later!")


