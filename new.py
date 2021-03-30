import datetime

timestamp = 1616667861215/1000
value = datetime.datetime.fromtimestamp(timestamp)
# year=value["%Y"]
print(value,'f')
print(f"{value:%Y-%m-%d %H:%M:%S}")

# print(datetime.datetime.fromtimestamp(timestamp).strftime('%c'))

from time import gmtime,strftime
import time

# print(time.ctime(timestamp/1000))
print(strftime("%a, %d %b %Y %H:%M:%S:%MS +0000", gmtime()))



import datetime
# s = 1236472051807 / 1000
s = 1616762086497/1000
# print(datetime.datetime.fromtimestamp(s).strftime('%a, %d %b %Y %H:%M:%S:.%fS')[:-3])
# print(datetime.datetime.fromtimestamp(s).strftime('%Y')[-2:])
year=datetime.datetime.fromtimestamp(s).strftime('%Y')[-2:]
print(year)
new=datetime.datetime.fromtimestamp(s).strftime(f'%a %m-%d-{year} %H:%M:%S.%f')[:-3] 
print(new)