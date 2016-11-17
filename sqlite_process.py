#!/usr/bin/python3

import sqlite3
import json

def tableparser(table):
	connection = sqlite3.connect(table)
	cursor = connection.cursor()

	# id: row[0]
	# device: row[1]
	# probe: row[2]
	# timestamp: row[3]
	# data: row[4]

	for row in cursor.execute("select * from data"):
		yield DataEntry(row)

	connection.close()

class DataEntry:
	def __init__(self, row):
		self.id = row[0]
		self.device = row[1]
		self.probe = row[2]
		self.timestamp = row[3]
		self.value = json.loads(row[4])
