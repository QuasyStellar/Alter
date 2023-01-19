import datetime

for i in range(35):
	current_date =  datetime.date.today() + datetime.timedelta(days=i)
	print(current_date)
