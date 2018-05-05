import datetime as dt

f1 = open('diary','w+')
f1.write("MY DIARY TRYOUT #1")
dNow = dt.datetime.now().day
mNow = dt.datetime.now().month
def switch(mNow):
	return {
		'1':'January',
		'2':'February',
		'3':'March',
		'4':'April',
		'5':'May',
		'6':'June',
		'7':'July',
		'8':'August',
		'9':'September',
		'10':'October',
		'11':'November',
		'12':'December',
	}[mNow]
mNowNew = switch(mNow)
yNow = dt.datetime.now().year
f1.write("\t"+str(dNow)+"-"+str(mNowNew)+"-"+str(yNow))
f1.close()
