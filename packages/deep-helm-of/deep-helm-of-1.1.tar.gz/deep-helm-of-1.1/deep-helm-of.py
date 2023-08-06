#!/usr/bin/env python
import string
import random
import time
string.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(1000000):
	for i in range(2):
		nnn = random.choice(string.letters)
		for i in range(23):
			print(nnn + random.choice(string.letters))
	print( "DAVID MART PIDORAS")
	print("SALEX JOPOLAZ")
	time.sleep(0.1)
	for i in range(10):
		print("HAHAHAHHAHAH")

