import mysql.connector
from mysql.connector import errorcode
import time
import datetime
import locale
import sys
import os

def create_transaction():
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
	
	os.system("clear")
	transaction_name = raw_input("What would you like to call this transaction? ")
	# ask again if user inputs empty string
	while (transaction_name == "" or len(transaction_name) > 100):
		os.system("clear")
		if (transaction_name == ""):	
			print("What would you like to call this transaction? ")
			transaction_name = raw_input("Sorry, the name can't be blank. Try again: ")
		else:
			print("What would you like to call this transaction? ")
			transaction_name = raw_input("Sorry, that name is too long. Try again: ")
	
	# get categories from categories db for options
	categories_query = ("SELECT name FROM categories")
	cursor.execute(categories_query)
	category_names = cursor.fetchall()
	category_counter = 0	
	selected_category_string = "Uncategorized"
	if len(category_names) > 0:
		print ("What category should this go under?")
		for category_name in category_names:	
			category_counter += 1
			print str(category_counter) + ". " + category_name[0]	
		valid_category = False
		while (not valid_category):
			try:
				selected_category = raw_input("Type the option number and hit <Enter>: ");
				selected_category_int = int(selected_category)
				if (selected_category_int < 1 or selected_category_int > category_counter):
					raise ValueError()
				valid_category = True
				selected_category_string = category_names[selected_category_int - 1][0]
			except ValueError:
				valid_category = False

	today = time.strftime("%y/%m/%d")
	today = "20" + today
	date = today
	# first ask if the transaction happened today
	print("Did this transaction happen today? (" + today + ")")
	user_response_today = raw_input("(Yes/No): ")
	while (user_response_today != "Yes" and user_response_today != "No"):
		user_response_today = raw_input("(Yes/No): ")
	# if transaction didn't happen today, ask when it happened
	if user_response_today == "No":
		can_parse_date = False
		# ask user for date and validate
		while (not can_parse_date):
			print("When did it happen?")
			date = raw_input("(YYYY/MM/DD): ")
			try:
				date_parts = date.split('/')
				# make sure input is in x/y/z format
				if len(date_parts) != 3:
					can_parse_date = False
					raise ValueError()
				if date > today:
					raise ValueError()
				# the line below will throw a ValueError if the date doesn't exist
				datetime.datetime(year = int(date_parts[0]), month = int(date_parts[1]), day = int(date_parts[2]))
				# if it gets to this point with no errors, date exists	
				can_parse_date = True
			except ValueError:
				can_parse_date = False

	can_parse_cost = False
	# set locale to dollars
	locale.setlocale(locale.LC_ALL, '')
	cost = 0
	cost_string = ""
	while not can_parse_cost:
		cost_string = raw_input("How much did " + transaction_name + " cost? ")
		cost_string = cost_string.replace("$", "")
		try:	
			# don't allow negative costs
			cost = float(cost_string)
			if cost < 0:
				raise ValueError()
			cost_string = locale.currency(cost, grouping = True)
			can_parse_cost = True
		except ValueError:
			can_parse_cost = False	

	note = raw_input("Any notes on this transaction? Hit <Enter> to skip: ")

	add_transaction = ("INSERT INTO transactions "
						"(date, name, category, cost, note)"
						"VALUES (%(date)s, %(name)s, %(category)s, %(cost)s, %(note)s)")
	transaction_data = { 'date' : date, 'name' : transaction_name, 'category' : selected_category_string, 'cost' : cost, 'note' : note }

	cursor.execute(add_transaction, transaction_data)

	cnx.commit()

	options = ["1", "2"]
	os.system("clear")
	print("Success! Transaction details: \n")
	print("\tName: " + transaction_name)
	print("\tCategory: " + selected_category_string)
	print("\tDate: " + date)
	print("\tCost: " + cost_string)
	print("\tNote: " + note)
	print("\n1. Back to Main Menu")
	print("2. Exit")
	selected_final_option = raw_input("Type the option number and hit <Enter>: ")
	while (not selected_final_option in options):
		os.system("clear")
		print("Success! Transaction details: \n")
		print("\tName: " + transaction_name)
		print("\tCategory: " + selected_category_string)
		print("\tDate: " + date)
		print("\tCost: " + cost_string)
		print("\tNote: " + note)
		print("\n1. Back to Main Menu")
		print("2. Exit")
		selected_final_option = raw_input("Sorry, that's not a valid option. Try again: ")
	
	if (selected_final_option == options[1]):
		os.system("clear")
		sys.exit("See you later!")

	cursor.close()
	cnx.close()
