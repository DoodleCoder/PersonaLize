import pyspeedtest
st = pyspeedtest.SpeedTest()
a=0
try:
	a = st.ping()
except:
	pass
print(a)