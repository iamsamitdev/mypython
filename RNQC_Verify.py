"""
Filename:       rn_verify.py
Date:           2014-05-20
Author:         C. Smith
Description:    RN Flash verify script.

#***********************************
NOVEMBER 7, 2014
S. Whitman
Changed version from 1.00 to 1.01
INITIAL SET FOR NAMUGA

# INITIAL SETUP WITH 10 RN171 MPC
XGA017YLXD32     RN171-I/RM232
XGA017YLXD36     RN171-I/RM236
XGA011YLXD40     RN171-I/RM400
XGA011YLXD41     RN171-I/RM441
XGA017YLXD00     RN171-I/RM
XGA017YLXD21     RN171R-I/RM406
XGA017YLXD27     RN171-I/RMSCT427
XGA017YLXD48     RN171-I/RMCEN248
XGA017YLXDCL     RN717-I/RMCEL240
XGA017YLXDLD     RN171-I/RMLDA122

# INITIAL SETUP WITH 15 RN131 MPC
XGA011YHXC00	   RN131C/RM
XGA011YHXC40	   RN131C/RM400
XGA011YHXC41	   RN131C/RM441
XGA011YHXDBS	   RN131C/RMBSC400
XGA011YHXC50	   RN131C/RMHWD350
XGA011YHXC27	   RN131C/RMIND227
XGA011YHXCFT	   RN131C/RMRFT117
XGA017YHXC00	   RN131G-I/RM
XGA017YHXC03	   RN131G-I/RM227
XGA017YHXC32	   RN131G-I/RM231
XGA017YHXC33	   RN131G-I/RM232
XGA017YHXCRM	   RN131G-I/RM400
XGA017YHXG41	   RN131G-I/RM441
XGA017YHXCBH	   RN131G-I/RMBHE211
XGA017YHXCQT	   RN131G-I/RMQTK200
#**********************************
December 15, 2014
S. Whitman
Changed version from 1.01 to 1.02
Adding two RN171 options
XGA017YLXD03	RN171S-I/RM407 - XGA017YLXD03-S407.bin
XGA011YLXD39	RN171-I/RM238  - XGA011YLXD39-2.38.bin
Adding one RN131 option
XGA017YHXC24	RN131G-I/RM245 - XGA017YHXC24-2.45.bin
#**********************************
Jan 29, 2015
S. Whitman
Changed version from 1.02 to 1.03
Added one RN171 option
XGA017YLXDLX	RN171-I/RMPLX232
#**********************************
March 27, 2015
S. Whitman
Changed version from 1.03 to 1.04
Added one RN131 option
XGA011YHXC36    RN131C/RM236

#**********************************
October 26, 2015
S. Whitman
Changed version from 1.04 to 1.05

Added two RN171 option
XGA017YLXD50     RN171-I/RMCEN250
XGA017YVXD75	RN171-I/RM475

Added two RN131 options
XGA011YHXC75	RN131C/RM475
XGA017YHXG75	RN131G-I/RM475
Note: will use the same bin file to
	reference both RN131 CPNs
	XGA017YHXG75-4.75.bin

#**********************************
#**********************************
#**********************************
#**********************************
"""
#!/usr/bin/python

import sys
import StringIO
from ftplib import FTP
import telnetlib
from datetime import datetime
import subprocess
import hashlib
import logging
import logging.handlers


#**********************************
# Globals
#**********************************
APP_VERSION = '1.05'
FIRMWARE_DIR = '../firmware/'
OUTPUT_DIR = '../output/'
TESTER_NW = '10.2.1.'
TESTER_IP = ''
LotID = ''

production_image = ''
scanMAC = True
opt = 0
test_logger = ''
prod_image_hash = ''


# *************************************************************
# Calculates the MD5 hash of the specified file
# *************************************************************
def md5_G2bin(file_name):
    #print "Calc MD5 for file: " + file_name
    config_FR = '\x01\x06\x63\x6F\x6E\x66\x69\x67'

    # Open,close, read file and calculate MD5 on its contents 
    file_to_check = open(file_name, "rb")
    
    md5 = hashlib.md5()

    # Skip past calibration sector 
    file_to_check.seek(0x1000)

    # Read through all sectors
    for sect in xrange(1,254): 

        data = file_to_check.read(0x1000)

        # Check if @ EOF if so fill with 0xFF
        if data == '':
            data = b'\xFF' * 0x1000
            #print "File has " + str(sect) + " sectors."

        # Check if wifly config file sector 
        if config_FR in data[7:32]:
            data = b'\xFF' * 0x1000
            #print "Found config file in sector: " + str(sect)

        md5.update(data)

    # Close the file
    file_to_check.close()

    return md5.digest()


# *************************************************************
# Reads the contents of the G2 flash and writes it to a file
# *************************************************************
def get_flash_binfile(tester_ip = TESTER_IP, imagefile = ''):
    ftp = FTP(tester_ip)
    ftp.login()
    flash_file = open(imagefile, 'wb')
    ftp.retrbinary('RETR ' + imagefile, flash_file.write)
    flash_file.close()
    ftp.quit()


def get_file(tester_ip = TESTER_IP, imagefile = ''):
    ftp = FTP(tester_ip)
    ftp.login()
    stream = StringIO.StringIO()
    ftp.retrlines('RETR ' + imagefile,  stream.write)
    ftp.quit()
    lines =  stream.getvalue()
    stream.close()
    return lines



# *************************************************************
# Verifies the flash contains a calibration.dat file 
# *************************************************************
def check_cal(tester_ip = TESTER_IP):
    ftp = FTP(tester_ip)
    ftp.login()
    ftp.cwd('flash.bin')
    files = ftp.nlst()
    ftp.quit()
    print files
    if 'v1.2.2' in files:
        print '\033[1;42m%s\033[0;39m' % 'Logicdatat V1.2.2'	
    have_cal = False
    if 'calibration.dat' in files:
        have_cal = True
    return have_cal


# *************************************************************
# Verifies the flash contents match the prodion bin file 
# *************************************************************
def verify_device():
    global file_md5
    global test_logger
    global TESTER_IP
    global LotID

    print '  '
    print '  '
    print "  File MD5 Hash: " + file_md5.encode('hex')

    # Read Device Flash Contents & wirte to file 'flash.bin'
    get_flash_binfile(tester_ip = TESTER_IP, imagefile = 'flash.bin')

    # Calculate device md5
    device_md5 = md5_G2bin('flash.bin')
    print "Device MD5 Hash: " + device_md5.encode('hex')

    # Check if md5's match
    print '  '
    # print (production_image)
    f = open('verify_MPC.txt','wb')
    f.write (production_image+'\n')
    f.close()
    # print '  '
    import os  
    os.system('echo =================================== >> $(date +%Y.%m.%d).log')
    os.system('echo Production image being verified:   >> $(date +%Y.%m.%d).log')
    os.system('cat verify_MPC.txt >> $(date +%Y.%m.%d).log')
    os.system('echo Reading_Module >> $(date +%Y.%m.%d).log')
    os.system('g2fs flash.bin list|egrep FILETIME_FR\|FILENAME_FR\|MAC_ADDRESS -m3 >> $(date +%Y.%m.%d).log')
    os.system('rm verify_MPC.txt')

    if file_md5 == device_md5:
        print '  '
        print '\033[1;42m%s\033[0;39m'% "MODULE PASSED VERIFY     PASS PASS PASS PASS     "
        test_logger.critical('******* MD5 Match; VERIFY PASS ******* \r\n')
        import os
        os.system('echo MD5 Match-VERIFY PASS >> $(date +%Y.%m.%d).log')
     
    else:
        print '  '
        print '\033[41;37m' "WARNING  WARNING  WARNING  WARNING  WARNING  WARNING  WARNING" '\033[0;39m'
        print '\033[41;37m' "                                                             " '\033[0;39m'
        print '\033[41;37m' "******* VERIFY FAILED!  FAIL  FAIL  FAIL  FAIL  FAIL  *******" '\033[0;39m'
        print '\033[41;37m' "                                                             " '\033[0;39m'
        print '\033[41;37m' "WARNING  WARNING  WARNING  WARNING  WARNING  WARNING  WARNING" '\033[0;39m'
        test_logger.critical('******* MD5 Mismatch; VERIFY FAIL ******* \r\n')
        import os
        os.system('echo MD5 Mismatch-VERIFY FAIL >> $(date +%Y.%m.%d).log')
        
# *************************************************************
# Display Application Menu Options
# NOTE:  Add new options as needed
#
# *************************************************************
def menu():
    print "==============================================="
    print "   RN131 Module QC Test Verification Program"
    print "==============================================="
    print "     "
    return raw_input ("SCAN MPC CODE TO FETCH PRODUCTION FIRMWARE  : ")
    print "     "


def set_prod_image(opt):
    global production_image


#----------------------------------------------------------
# Set Production image file name
# NOTE: Added new Production Images to the list as needed
#
# Initial release Nov 7, 2014.  
# Note RN171 MPC XGA011YLXD41, XGA017YLXD00 will use the same XGA011YLXD41-4.41.bin 4.41 image   
# Note RN131 MPC XGA011YHXC41, XGA011YHXC00, XGA017YHXG41, XGA017YHXC00 will use the same #XGA011YHXC41-4.41.bin 4.41 image 
#
#----------------------------------------------------------
    
    if opt == 'XGA011YHXC36':
        production_image = 'XGA011YHXC36.bin'
    if opt == 'XGA011YHXC41':
        production_image = 'XGA011YHXC41.bin'
    if opt == 'XGA011YHXC00':
        production_image = 'XGA011YHXC00.bin'
    if opt == 'XGA011YHXC81':
        production_image = 'XGA011YHXC81.bin'
    if opt == 'XGA011YHXC75':
        production_image = 'XGA017YHXG75.bin'
    if opt == '   ':
        production_image = '=============================='
    if opt == 'XGA011YHXC27':
        production_image = 'XGA011YHXC27.bin'
    if opt == 'XGA011YHXC50':
        production_image = 'XGA011YHXC50.bin'
    if opt == 'XGA011YHXCFT':
        production_image = 'XGA011YHXCFT.bin'
    if opt == 'XGA011YHXDBS':
        production_image = 'XGA011YHXDBS.bin'
    if opt == '   ':
        production_image = '=============================='
    if opt == 'XGA017YHXC03':
        production_image = 'XGA017YHXC03.bin'
    if opt == 'XGA017YHXC24':
        production_image = 'XGA017YHXC24.bin'
    if opt == 'XGA017YHXC32':
        production_image = 'XGA017YHXC32.bin'
    if opt == 'XGA017YHXC33':
        production_image = 'XGA017YHXC33.bin'
    if opt == 'XGA017YHXCRM':
        production_image = 'XGA017YHXCRM.bin'
    if opt == 'XGA017YHXG41':
        production_image = 'XGA017YHXG41.bin'
    if opt == 'XGA017YHXC00':
        production_image = 'XGA017YHXC00.bin'
    if opt == 'XGA017YHXG75':
        production_image = 'XGA017YHXG75.bin'
    if opt == 'XGA017YHXCBH':
        production_image = 'XGA017YHXCBH.bin'
    if opt == 'XGA017YHXG81':
        production_image = 'XGA017YHXG81.bin'

 #----------------------------------------------------------


def runTest():
    global test_logger
    global TESTER_IP
    import os

    print "Tester IP: " + TESTER_IP

    while 1:
        if scanMAC:
            print '_______________________________________________________'
            devMAC = raw_input("Place Module and Close the lid to start. Then hit ENTER: ")
            print '\n'
            test_logger.info('MAC Addr: ' + devMAC)
        else:
            raw_input("Press ENTER to begin: ")

        # Make sure tester Lid is "Closed"
        if '1' in get_file(tester_ip = TESTER_IP, imagefile = 'lid.txt'):
            print '   '
            print '     The lid is open or no module is inserted.'
            test_logger.warning('Lid open or No module inserted')
            continue

        # Query Module Flash Part#
        flash_type = get_file(tester_ip = TESTER_IP, imagefile = 'device.txt')
        print "Flash Type: " + flash_type

        if 'device size is 8 Mbits' not in flash_type:
            print '\033[41;37m' 'Flash device is unrecognized: %s' '\033[0;39m' % flash_type
            test_logger.error('Unrecognized Flash Device')
            continue

        # Verify module has calibration file
        if check_cal(tester_ip = TESTER_IP):
            # Verify flash matches file
            verify_device()

            # Verify Device MAC Address
            # TODO:  Add this test

        else:
            print '\033[41;37m' 'Module is Untested and Memory is Blank or Corrupted' '\033[0;39m'
            test_logger.error('Module is Untested and Memory is Blank or Corrupted')
            os.system('echo Blank Memory - FAIL >> $(date +%Y.%m.%d).log')
        print '\r\n'
        
        choice = str(raw_input("\nNext Module [y/n]?  "))  

        if choice == "y" or choice == "Y" or choice == "Yes" or choice == "yes": 
           continue
        else:
            choice = str(raw_input("\nAre you sure you want to End Lot [y/n]? "))
            if choice == "n" or choice == "No" or choice == "N" or choice == "no":
               continue
            else: 
                print "\nLot has ended testing. Creating Lot Summary Report...."
                os.system('sleep 1')
                os.system('../OI/QCEndLot.sh')
                exit()
                

def main():
    global opt
    global production_image
    global scanMAC
    global test_logger
    global file_md5
    global TESTER_IP
    global LotID


    # Setup Tester IP Address
    
    testerID = raw_input("Enter Tester ID (last 3 character of TF IP address):")
    TESTER_IP = TESTER_NW + testerID

    # Setup Log File
    test_logger = logging.getLogger('st427')
    test_logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler = logging.handlers.TimedRotatingFileHandler(OUTPUT_DIR + 'logID-' + testerID, when='midnight')
    handler.setFormatter(formatter)
    test_logger.addHandler(handler)

    # Display Menu and get option to run
    opt = menu()
    
    set_prod_image(opt)

    # Ask if test should ask for MAC Address
#    choice = raw_input("Scan MAC Address(Yes/No)?  ").lower()

#    yes = set(['yes','y', 'ye', ''])
#    no = set(['no','n'])

#    if choice in yes:
#        scanMAC = True
#    elif choice in no:
#        scanMAC = False
#    else:
#        sys.stdout.write("Please respond with 'yes' or 'no'")

#    print "Scan Barcode: " + str(scanMAC)
    
    scanMAC = True

    test_logger.info('----------------------------------------------------')
    test_logger.info('*********** Begin Test Session *********************')
    test_logger.info('Verify Test Application version ' + APP_VERSION)
    test_logger.info('Date/Time: ' + str(datetime.now().time()))
    test_logger.info('Test image: ' + production_image)
    #test_logger.info('Scan Barcode: ' + str(scanMAC))

    #test = md5_G2bin('flash.bin')
    #print "Flash md5: " + str(test)

    # Calculate file md5
    file_md5 = md5_G2bin(FIRMWARE_DIR + production_image)
    print "File MD5 Hash: " + file_md5.encode('hex')
    test_logger.info('File MD5: ' + file_md5.encode('hex'))
    test_logger.info('----------------------------------------------------')

    runTest()

    return


if __name__ == "__main__":
    main()


