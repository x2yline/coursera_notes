import os
import sys
import tinify

tinify.key = 'eB0lNVNaiSmvH3HMG8sXkqn8t8dSsqS5'
print 'The size of picture must smaller than 5M!!!!!!!!!!!!'
listfile=os.listdir(os.getcwd())
try:
	for line in listfile:
		if line.split('.')[-1] == 'jpg' or line.split('.')[-1] == 'png':
			print 'begin for file optimizing ' + line

			tinify.from_file(line).to_file(line.split('.')[0] +  '_optmized'+'.'+line.split('.')[-1])
			print('file optimized to ' + line.split('.')[0] + '_optmized'+'.'+line.split('.')[-1])

	raw_input('all things have been done!!!')
except:
	raw_input('something wrong have occured')




