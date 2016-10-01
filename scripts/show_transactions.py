from prettytable import PrettyTable
import mysql.connector
import sys
import os

def delegate_show_transactions(sort_column, desc):
	show_transactions(sort_column, desc, False)	# default sorting
	show_transactions_options()

def show_transactions(sort_column, desc, show_id):
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

	if sort_column == "date":
		get_transactions = ("SELECT * FROM transactions ORDER BY date")
	elif sort_column == "name":
		get_transactions = ("SELECT * FROM transactions ORDER BY name")
	elif sort_column == "category":
		get_transactions = ("SELECT * FROM transactions ORDER BY category")
	elif sort_column == "cost":
		get_transactions = ("SELECT * FROM transactions ORDER BY cost")
	else:
		raise ValueError()
	if desc:
		get_transactions += " DESC"
	get_transactions += ", date DESC"	# secondary sort by date desc
	cursor.execute(get_transactions)
	transaction_query_results = cursor.fetchall()
	
	os.system("clear")
	if len(transaction_query_results) == 0:
		print "There's nothing here! Use the main menu to add a transaction."
	else:
		pretty_table = PrettyTable()
		if show_id:
			pretty_table.field_names = ['ID', 'Date', 'Name', 'Category', 'Cost', 'Note']
		else:
			pretty_table.field_names = ['Date', 'Name', 'Category', 'Cost', 'Note']
		for transaction in transaction_query_results:
			if show_id:
				pretty_table.add_row([transaction[0], str(transaction[1]).replace('-', '/'), transaction[2], transaction[3], '${:,.2f}'.format(transaction[4]), transaction[5]])
			else:
				pretty_table.add_row([str(transaction[1]).replace('-', '/'), transaction[2], transaction[3], '${:,.2f}'.format(transaction[4]), transaction[5]])
	print(pretty_table)

	# close stuff
	cursor.close()
	cnx.close()

def show_transactions_options():
	post_show_options = ["1", "2", "3"]
	print("\n1. Sort")
	print("2. Back to Main Menu")
	print("3. Exit")
	selected_final_option = raw_input("Type the option number and hit <Enter>: ")
	while (not selected_final_option in post_show_options):
		os.system("clear")
		if len(transaction_query_results) == 0:
			print "There's nothing here! Use the main menu to add a transaction."
		else:
			for row in pretty_rows:
				print table_divider
				print row
			print table_divider
		print("\n1. Sort")
		print("2. Back to Main Menu")
		print("3. Exit")
		selected_final_option = raw_input("Sorry, that's not a valid option. Try again: ")
	
	if (selected_final_option == post_show_options[0]):
		sort_options = ["1", "2", "3", "4", "5", "6", "7", "8"]
		os.system("clear")
		print ("1. Date (Recent -> Old)")
		print ("2. Date (Old -> Recent)")
		print ("3. Name (A -> Z)")
		print ("4. Name (Z -> A)")
		print ("5. Category (A -> Z)")
		print ("6. Category (Z -> A)")
		print ("7. Cost (High -> Low)")
		print ("8. Cost (Low -> High)")
		selected_sort_option = raw_input("\nHow would you like to sort? Type the option number and hit <Enter>: ")
		while (not selected_sort_option in sort_options):
			os.system("clear")
			print ("1. Date (Recent -> Old)")
			print ("2. Date (Old -> Recent)")
			print ("3. Name (A -> Z)")
			print ("4. Name (Z -> A)")
			print ("5. Category (A -> Z)")
			print ("6. Category (Z -> A)")
			print ("7. Cost (High -> Low)")
			print ("8. Cost (Low -> High)")
			selected_sort_option = raw_input("\nSorry, that's not a valid option. Try again: ")
		if selected_sort_option == "1":
			delegate_show_transactions("date", True)
		elif selected_sort_option == "2":
			delegate_show_transactions("date", False)
		elif selected_sort_option == "3":
			delegate_show_transactions("name", False)
		elif selected_sort_option == "4":
			delegate_show_transactions("name", True)
		elif selected_sort_option == "5":
			delegate_show_transactions("category", False)
		elif selected_sort_option == "6":
			delegate_show_transactions("category", True)
		elif selected_sort_option == "7":
			delegate_show_transactions("cost", True)
		elif selected_sort_option == "8":
			delegate_show_transactions("cost", False)
		else:
			raise ValueError()
	elif (selected_final_option == post_show_options[2]):
		os.system("clear")
		sys.exit("See you later!")

