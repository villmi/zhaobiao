import traceback
import sys

a = 10
b = 0
fp = open("fp.log", "a")
try:
    print(a/b)
except Exception as e:
    traceback.print_exc(file=fp)
    # print(sys.exc_info())
print("1")
