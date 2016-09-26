from prettytable import PrettyTable
import mysql.connector
import sys
import os
import re

def show_analysis():
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
	date_pattern = re.compile('[0-9]{4}/[0-9]{2}/[0-9]{2}')
	start_date = raw_input("Start (YYYY/MM/DD): ")
	if start_date != "":
		date_match = re.match(date_pattern, start_date)
		if not date_match:
			raise ValueError("The date is not in the correct format.")
	end_date = raw_input("End (YYYY/MM/DD): ")
	if end_date != "":
		date_match = re.match(date_pattern, end_date)
		if not date_match:
			raise ValueError("The date is not in the correct format.")
	
	all_dates = start_date == "" and end_date == ""
	if all_dates:
		query = "SELECT SUM(cost) FROM transactions"
	else:
		query = "SELECT SUM(cost) FROM transactions WHERE date BETWEEN '{0}' and '{1}'".format(start_date, end_date)
	cursor.execute(query)
	total_cost = cursor.fetchone()[0]
	print("\nTotal spent: {0}".format('${:,.2f}'.format(total_cost)))

	pretty_table = PrettyTable()
	pretty_table.field_names = ['Category', 'Total Spent', '% of Total']
	if all_dates:
		query = "SELECT category, SUM(cost) AS total_cost FROM transactions GROUP BY category ORDER BY total_cost desc"
	else:
		query = "SELECT category, SUM(cost) AS total_cost FROM transactions WHERE date BETWEEN '{0}' and '{1}' GROUP BY category ORDER BY total_cost desc".format(start_date, end_date)
	cursor.execute(query)
	total_cost_by_category = cursor.fetchall()
	for item in total_cost_by_category:
		pretty_table.add_row([item[0], '${:,.2f}'.format(item[1]), '{:,.2f}%'.format(item[1] / total_cost * 100)])
	print(pretty_table)

	options = ["1", "2"]
	print("\n1. Back to main menu")
	print("2. Exit")
	selected_option = raw_input("Type the option number and hit <Enter>: ")
	while (selected_option not in options):
		print(pretty_table)
		print("\n1. Back to main menu")
		print("2. Exit")
		selected_option = raw_input("Sorry, that's not a valid option. Try again: ")

	if (selected_option == options[1]):
		os.system("clear")
		sys.exit("See you later!")

	cursor.close()
	cnx.close()
