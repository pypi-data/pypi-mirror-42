#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   Funcs
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 2019/03/01
#──────────────────────────
# discription:
#          operation between local PC with a remote server
#          remember to call connect or disconnect for some function.
#
#──────────────────────────
# Imported :
import os  
#──────────────────────────
# Interface:
#
#        [fun] readConfig(path)
#              return a dict used for paramiko  
# 
#        [sub] mkConfig(path)
#              create a new configuration file.    
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

class Funcs():
    
    @staticmethod
    def readConfig(path): 
        if os.path.isfile(path):
            return eval(open(path,'r').read())
        else:
            return "error: configurate file: {} not exist".format(path)
            
    
    @staticmethod
    def mkConfig(path):
        S = """
{
#-----------------------------------------------------------------------
#----------------------- START INPUT -----------------------------------

# -----[[ hostname ]]
# The hostname of the remote server, it can be an either an IP or DNS address
    "hostname" : "ec2-52-82-68-87.cn-northwest-1.compute.amazonaws.com.cn"  ,

# ----[[ Username ]]  
# Username of the remote server.
    "username" : "hadoop"  ,

# ----[[ Port ]]  
# Port number. Default value is 22.  
#    "port"     :  22       ,

# ----[[ password ]]  
# Optional input. If you can login by a password, input it.  
# "password"   :  'FLVFjn17cxpdGEWQ2S3nC26_0U1KYO'   ,

# ----[[ key_filename]]  
# Optional input. If you can login by a keyfile, input it. MUST be absolute path.  
  'key_filename'  :  'Dropbox/Desktop/AWS_NH_exercise/workout/CLI_created_key.pem' ,

#----------------------- END INPUT -------------------------------------
#-----------------------------------------------------------------------
} 
        """
        open(path,'w').write(S)
        
        
        
         
        
