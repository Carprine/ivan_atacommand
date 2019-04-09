import sys
import os
import io
import difflib
import re
import time
from sys import argv
import ata_common_func as ata

len_diff = 0
def compare(file1_name,file2_name,sata_dev):
    global len_diff
    print 'now compare data'
    with open(file1_name,'r') as file1,open(file2_name,'r') as file2:
        diff = difflib.unified_diff(file1.readlines()[1:33],file2.readlines()[1:33],fromfile=file1_name,tofile=file2_name)
        #print dir(diff)
        diff_list = list(diff)
    for diff_list_arg in diff_list:
        #print "diff_list_arg is:", "".join(diff_list_arg)
        if (re.findall(r"\++\[","".join(diff_list_arg)) or re.findall(r"\++MON","".join(diff_list_arg)) or re.findall(r"\++pHal","".join(diff_list_arg))):            
            len_diff = len_diff + 1
    print "len_diff is", len_diff
    if len_diff < 20:
        print "SATA test PASS"
        
        # Send Report
        ata.report_test_result_FAh(sata_dev, 0x1, 0x0)
        
        return 0
    else:
        for line in diff:
            sys.stdout.write(line)
        ata.report_test_result_FAh(sata_dev, 0x1, 0x1)
        return -1


def get_nand_status(sata_dev):
    cnt=19
    nand_ready = 0
    while(cnt>0):
        os.system("dd if="+sata_dev+" of=nandstatus.txt bs=512 count=1")
        with open("nandstatus.txt",'r') as statusfile:
            line=statusfile.readline()
            if line[0:9] != "readready":
                time.sleep(1)
                print "nand not ready"
            else:
                print "nand ready: tried %d times" % (19-cnt)
                nand_ready = 1
            statusfile.close()
        cnt -=1
        if nand_ready == 1:
            break
    if nand_ready == 0:
        print "NAND long time not ready"
        os.system("dd if=fail.txt of="+sata_dev)
        exit()
#Run command: python sata_test.py /dev/sdb nandon
#
python_file,sata_dev,nand=argv
print "python file is",python_file
print "sata_dev is ", sata_dev
print "nand is", nand
print("sata test")

val=os.system("ls "+sata_dev)
count=0
while val>0:
    val=os.system("ls "+sata_dev)
    count+=1
    time.sleep(1)
    if count > 100:
        print "device"+sata_dev+"not exist"
        quit()

print val
if val==0:
    os.system("rm output.txt")
    os.system("rm nandstatus.txt")

    #Write
    #output=os.system("dd if=input.txt of="+sata_dev+" bs=512 count=32")
    ata.write_dma_CAh('/dev/sdb', 'input.txt', 32, 0)
    
    if nand=='nandon':
        get_nand_status(sata_dev)
        #os.system("dd if=startReading.txt of="+sata_dev)
        time.sleep(3)
    print "reading" 

    #Read
    #os.system("dd if="+sata_dev+" of=output.txt bs=512 count=32")
    ata.read_dma_C8h('/dev/sdb', 'output.txt', 32, 0)
    
    if nand=='nandon':
        time.sleep(5)
    compare("output.txt","input.txt",sata_dev)
