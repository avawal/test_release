#!/usr/bin/ptyhon
import json
import subprocess
import logging
import os,sys
sys.path.append('./tests/utils/')
from mppv2 import executeShellCommand
from pprint import pprint

def login(password):
    cmd = ['docker', 'login', '-u', 'token', '-p', password , 'na.cumulusrepo.com']
    stdout, stderr, status = executeShellCommand(cmd, workdir=None)
    if stderr:
        logging.warning("Couldn't login to na.cumulusrepo.com: %s", stdout)
    logging.debug("Logged into na.cumulusrepo.com")
    return stderr == 0

def get_latest_image(container , image):
    '''
    Get latest wv-scripts image cumulus repo
    '''
  #  password='4636bab35b958a219c7d1ebbf5bd91e0'
    password=os.environ['CUMULUS-DEVELOP-PASSWORD']
    if login(password) == 0:
        TAG='na.cumulusrepo.com/dashdb_mppv2_develop/' + container + ':' + image
        cmd = [ 'docker', 'pull', TAG ]
        retry = 0
        while retry < 4:
                stdout, stderr, status = executeShellCommand(cmd, workdir=None)
                if not stderr:
                        logging.debug("Got 'docker pull %s' = %s", TAG, stdout)
                        return True
                else:
                        retry = retry + 1
                        logging.warning("Couldn't pull %s: %s ... retrying ", TAG, stdout)
    return False

def get_image_ID(container , image):
    '''
    Get the image ID for tagging the image 
    '''
    TAG='na.cumulusrepo.com/dashdb_mppv2_develop/' + container + ':' + image
    cmd = ['docker', 'images', '--format', '{{.ID}}', TAG] 
    stdout, stderr, status = executeShellCommand(cmd, workdir=None)
    return stdout

def tag_image(image_ID,TAG):
        '''
        Get the image and tag it to mppv2-latest repository
        '''
        cmd = ['docker', 'tag' , image_ID, TAG ] 
        stdout, stderr, status = executeShellCommand(cmd, workdir=None)
        if not stderr:
                logging.debug("Got 'docker tag %s' = %s", TAG, stdout)
        logging.warning("Couldn't tag  %s: %s", TAG, stdout)

def push_image(container,image,image_ID):
       '''
       Get the image and push it to mppv2-latest repository
       '''
       password=os.environ['CUMULUS-LATEST-PASSWORD']
       if login(token_pw) == 0:
                TAG='na.cumulusrepo.com/dashdb_mppv2_latest/' + container + ':' + image
                tag_image(image_ID, TAG)
                cmd = ['docker', 'push', TAG ] 
                retry = 0
                while retry < 4:
                        stdout, stderr, status = executeShellCommand(cmd, workdir=None)
                        if not stderr:
                                logging.debug("Got 'docker push  %s' = %s", TAG, stdout)
                                return True
                        else:
                                retry = retry + 1
                                logging.warning("Couldn't push  %s: %s", TAG, stdout)
       return False 

if __name__ ==  '__main__' :
      with open('entrypoint.txt') as f:
              entrypoint = [ int(x) for x in list(set(f)) ]
              entrypoint.sort()
              for line in range (0,7):
                      if line not in entrypoint:
                              exit(1)
      container_list = ["aspera", "monitoring" , "consolev2" ] #add dashdb to this list once completed 
      for container in container_list:
              data = json.load(open('mppv2_artifact.json'))
              image = data["service"]["containers"][container]["image_tag"]
              out = get_latest_image(container,image) 
              image_ID = get_image_ID(container,image)
              print image_ID

#              push_image(container,image,image_ID)


      
      


