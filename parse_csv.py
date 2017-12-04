import csv

with open('College_Statuses.csv', 'r') as f:
	reader = csv.reader(f, delimiter = ",")
	for row in reader:
		print row[0][1]