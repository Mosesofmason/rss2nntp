# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 16:12:38 2017

"""

import os
from nntplib import *
#from nntplib import NNTP_SSL

directory = "./outdir/"


try:
    ns = NNTP ('nntp.aioe.org')
    #ns = NNTP_SSL ('news.mixmin.net')
    ns.set_debuglevel(1)
    
    n=0
    
    for file in os.listdir(directory):
        if file.endswith(".eml"):          
            try:
                print(os.path.join(os.linesep + directory, file) + os.linesep)
                f = open(os.path.join(directory, file))
                if n<10:
                    time.sleep(2*n)
                else:
                    time.sleep(600)
                ns.post(f) 
                f.close()
                n = n+1
                os.remove (os.path.join(directory, file))
            except NNTPTemporaryError:
                print ('duplicated article')               
                f.close()     
                os.remove (os.path.join(directory, file))
                continue

finally:
    # Close the usenet connection.
    response = ns.quit()
    # Print the response.
    print(response)