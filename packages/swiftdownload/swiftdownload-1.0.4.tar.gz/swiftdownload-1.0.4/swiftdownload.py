import logging
import datetime
import time
import os
import uuid
import shutil
import click
import subprocess
from swiftclient.service import SwiftService, SwiftError
from sys import argv
logging.basicConfig(level=logging.ERROR)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("swiftclient").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
now = datetime.datetime.now()


#os.environ['OS_USERNAME'] = sw_stf
#os.environ['OS_PASSWORD'] = '6Ziff3CslR5Nei9B'
#os.environ['OS_TENANT_NAME'] = sw_stf
#os.environ['OS_AUTH_URL'] = 'https://cdc-keystone-endpoint.prod.walmart.com:5000/v2.0'
#os.environ['OS_REGION_NAME'] = 'cdc-obj-photon-102'
#os.environ['SWIFTCLIENT_INSECURE'] = false

os.putenv("OS_USERNAME", "sw_stf")
os.putenv("OS_PASSWORD", "6Ziff3CslR5Nei9B")
os.putenv("OS_TENANT_NAME", "sw_stf")
os.putenv("OS_AUTH_URL", "https://cdc-keystone-endpoint.prod.walmart.com:5000/v2.0")
os.putenv("OS_REGION_NAME", "cdc-obj-photon-102")
os.putenv("SWIFTCLIENT_INSECURE", "false")
#subprocess.call("/u/myproject/s.sh") 


#pathToday = 'report/topic_1/'+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'+'latest/generic-oneops'
def move_files(dest_folder, file_path, mdomid,file_name):
    #print dest_folder
    #print file_path
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_folder = dest_folder +'/'+str(uuid.uuid4())
    if file_path.find(mdomid) != -1:
        #Move to desination folder with name
        shutil.move(file_path, dest_folder+file_name)

def combine_file(file_path, file_name):
    if os.path.isfile(file_path+"/"+file_name):
        os.remove(file_path+"/"+file_name)
        print("File deleted " + str(file_path+"/"+file_name))
    file_output = os.path.join(file_path,file_name)
    files = os.listdir(file_path)
    for file in files:
        os.path.join(file_path,file)
        f = open(os.path.join(file_path,file),'r') 
        fout = open(file_output,"a")
        for line in f:
           fout.write(line)


def is_png(obj,mdom_name,pathToday):
    if (obj["name"].find(pathToday) != -1) and (obj["name"].find(mdom_name) != -1) and obj["name"].lower().endswith('.csv'):
       print(str(obj["name"].lower()))
       return True
    else:
       return False

@click.command()
@click.option('-m', '--mdom_name', multiple=False)
@click.option('-c', '--container', multiple=False)
@click.option('-df', '--destination_folder', multiple=False)
@click.option('-cf', '--csv_filename',multiple=False)
@click.option('-t', '--topic',multiple=False)
def download_script(mdom_name,container,destination_folder,csv_filename,topic):
    with SwiftService() as swift:
        try:
            os.putenv("OS_USERNAME", "sw_stf")
            os.putenv("OS_PASSWORD", "6Ziff3CslR5Nei9B")
            os.putenv("OS_TENANT_NAME", "sw_stf")
	    os.putenv("OS_AUTH_URL", "https://cdc-keystone-endpoint.prod.walmart.com:5000/v2.0")
            os.putenv("OS_REGION_NAME", "cdc-obj-photon-102")
	    os.putenv("SWIFTCLIENT_INSECURE", "false")
            #subprocess.call("/u/myproject/s.sh",shell=True) 
            list_options = {"prefix": "path"}
            list_parts_gen = swift.list(container=container)
            for page in list_parts_gen:
                pathToday = 'report/'+topic+'/'+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'+container+'/'+mdom_name
                if page["success"]:
                    objects = [
                        obj["name"] for obj in page["listing"] if is_png(obj,mdom_name,pathToday)
                    ]
            #print "Objects" + str(objects);
                    for down_res in swift.download(container=container,objects=objects):
                        if down_res['success']:
                            print("'%s' downloaded" % down_res['object'])
                        else:
                            print("'%s' download failed" % down_res['object'])
                    try:
                        os.system("rm -rf " + destination_folder + "*.csv")
                    except Exception as e:
                        print("Directory doesn't exist" + str(destination_folder))
                    for obj in objects:
                         move_files(destination_folder, obj,mdom_name,csv_filename)
                    combine_file(destination_folder,csv_filename)
		    click.echo('download sucessful')
                else:
                    raise page["error"]
        except SwiftError as e:
            logger.error(e.value)
if __name__=='__main__':
	download()
