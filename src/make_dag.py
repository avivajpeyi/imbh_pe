import numpy as np
import sys
'''
Usage: 
python create_dag.py 5   

Creates 5 BNS injections
'''
number_of_simulations = int(sys.argv[1])

for i in range(0,number_of_simulations): 
    file = open('inj_bbhpop.dag','a')
    idx  = i 
    file.write('Job '+str(idx)+' inj_bbhpop.sub \n')
    file.write('VARS '+str(idx)+' jobNumber="'+str(idx)+'" ')
    file.write('\n')
    file.close()
    
    
for i in range(1,number_of_simulations):
    file = open('inj_bbhpop.dag','a')
    #file.write(' ' + str(i))
    file.close()

