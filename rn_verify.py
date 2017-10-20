"""
Filename:       rn_verify.py
Date:           2014-05-20
Author:         C. Smith
Description:    RN Flash verify script.
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
APP_VERSION = '1.00'
FIRMWARE_DIR = 'firmware/'
OUTPUT_DIR = 'output/'
TESTER_NW = '10.2.1.'
TESTER_IP = '' 

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

    print "File MD5 Hash: " + file_md5.encode('hex')

    # Read Device Flash Contents & wirte to file 'flash.bin'
    get_flash_binfile(tester_ip = TESTER_IP, imagefile = 'flash.bin')

    # Calculate device md5
    device_md5 = md5_G2bin('flash.bin')
    print "Device MD5 Hash: " + device_md5.encode('hex')

    # Check if md5's match
    if file_md5 == device_md5:
        print '\033[1;42m%s\033[0;39m'%"PASS - MD5 verified."
    else:
        print '\033[41;37m' "FAIL - MD5 failed!." '\033[0;39m'
        test_logger.critical('MD5 Mismatch\r\n')



# *************************************************************
# Display Application Menu Options
# NOTE:  Add new options as needed
# *************************************************************
def menu():
    print "==============================================="
    print " RN Production Verify Test Application Ver: %s \r\n" % APP_VERSION
    print " Choose option to run:"
    print "==============================================="
    print " 0)  LogicData 2.00"
    print " 1)  RN-171 Wifly 4.01"
    print " 2)  MCW-1283 Rel 1.00"
    print " 3)  Scantool Rel 4.27"
    print " 4)  RN-171 Wifly 4.41"
    print " 5)  Centrak 2.48"
    print " 6)  RN-171 Wifly 2.32"

    return raw_input ("Choose option: ")


def set_prod_image(opt):
    global production_image


    #----------------------------------------------------------
    # Set Production image file name
    # NOTE: Added new Production Images to the list as needed
    #----------------------------------------------------------
    if opt == '0':
        production_image = 'logicdata-200.bin'
    if opt == '1':
        production_image = 'RN-171_wifly7-4001.bin'
    if opt == '2':
        production_image = 'MCW1283-100.bin'
    if opt == '3':
        production_image = 'SCT-427.bin'
    if opt == '4':
        production_image = 'RN-171_wifly7-441.bin'
    if opt == '5':
        production_image = 'CENTRAK-248.bin'
    if opt == '6':
        production_image = 'RN-171_wifly7-232.bin'

    #----------------------------------------------------------


def runTest():
    global test_logger
    global TESTER_IP

    print "Tester IP: " + TESTER_IP

    while 1:
        if scanMAC:
            devMAC = raw_input("Close the lid to start: ")
            test_logger.info('MAC Addr: ' + devMAC)
        else:
            raw_input("Press ENTER to begin: ")

        # Make sure tester Lid is "Closed"
        if '1' in get_file(tester_ip = TESTER_IP, imagefile = 'lid.txt'):
            print '\033[41;37m' 'The lid is open or no module is inserted.' '\033[0;39m'
            test_logger.warning('Lid open or No module inserted')
            continue

        # Query Module Flash Part#
        flash_type = get_file(tester_ip = TESTER_IP, imagefile = 'device.txt')
        print "Flash Type: " + flash_type

        if 'device size is 8 Mbits' not in flash_type:
            print '\033[41;37m' 'Flash device is unrecognized: %s' '\033[0;39m' % flash_type
            tester_logger.error('Unrecognized Flash Device')
            continue

        # Verify module has calibration file
        if check_cal(tester_ip = TESTER_IP):
            # Verify flash matches file
            verify_device()

            # Verify Device MAC Address
            # TODO:  Add this test

        else:
            print '\033[41;37m' 'calibration file NOT found' '\033[0;39m'
            test_logger.error('Calibration file NOT found')

        print '\r\n'


def main():
    global opt
    global production_image
    global scanMAC
    global test_logger
    global file_md5
    global TESTER_IP


    # Setup Tester IP Address
    testerID = raw_input("Tester ID:")
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

