import sys
import subprocess
import datetime
import ConfigParser
from xlrd import open_workbook

#define global
SCENE_NAME = ''
CMD_DIR = ''
LOG_DIR = ''
SEVERITY = ''
message = []
device_list = []
Config = ConfigParser.ConfigParser()

def getIP(msg):
	start = msg.find('[')
	end = msg.find(']')
	return msg[start + 1:end]


def callUDCV():
	timestamp = str(long((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds()*1000))
	ipaddress = getIP(message[1])
	print "ipaddress = " + ipaddress
	if len(ipaddress) < 1:
		print "fail to get ipaddress from trap message, please check " + LOG_DIR + "for more infomation \n"
		return
	deviceID = findDeviceByIP(ipaddress)
	print "deviceID = " + deviceID
	if deviceID == 'not found':
		print "fail to get deviceID from asset file %s, please check %s for more infomation \n" % (ASSET, LOG_DIR)
		return
	title = message[2]
	body = message [3]
	command = """event.bat ECC _ %s "%s" OPEN %s "%s" %s %s _ _""" % (deviceID, title, SEVERITY, body, timestamp, timestamp)
	p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, cwd = CMD_DIR)
	stdout, stderr = p.communicate()
	print stdout

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def findDeviceByIP(ipaddress):
	for record in device_list:
		if (record['mngt_ip'] == ipaddress):
		  return record['ID']
	return 'not found'

def init():
	Config.read("./trap.conf")
	global SCENE_NAME,CMD_DIR,LOG_DIR,SEVERITY
	SCENE_NAME = ConfigSectionMap("General")['scene_name']
	CMD_DIR = ConfigSectionMap("General")['cli_path']
	LOG_DIR = ConfigSectionMap(SCENE_NAME)['log_path']
	SEVERITY = ConfigSectionMap(SCENE_NAME)['default_severity']
	ASSET = ConfigSectionMap(SCENE_NAME)['asset_path']
	wb = open_workbook(ASSET)
	rackDeviceSheet = wb.sheet_by_name('rackDevice')

	# read header values into the list    
	keys = [rackDeviceSheet.cell(0, col_index).value for col_index in xrange(rackDeviceSheet.ncols)]

	for row_index in xrange(1, rackDeviceSheet.nrows):
		d = {keys[col_index]: rackDeviceSheet.cell(row_index, col_index).value for col_index in xrange(rackDeviceSheet.ncols)}
		device_list.append(d)

def main():
	init()
	running = True
	print "LOG_DIR = " + LOG_DIR
	output = open(LOG_DIR, 'a')
	index = 0
	while running:
		try:
			input = raw_input()
			message.append(input)
			output.write(input + "\n")
		except EOFError:
			running = False
	print message
	output.close()
	callUDCV()


if __name__ == '__main__':
	main()