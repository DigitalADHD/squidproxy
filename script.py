#!/usr/bin/env python
# -*- utf8-encoding -*-

import os
import re
from time import gmtime, strftime
import sys

# date and time
def date_time():
	return strftime("%Y-%m-%d %H:%M:%S", gmtime()); # return data with Year-month-day Hour-minute-second
# Append data on existing file
def write_to_file(filename, text):
	with open(filename, mode='a+') as outfile:
		outfile.write("%s\n" % text)
		outfile.close()

dir_="/etc/squid3"
squid = "squid.conf"
commands="""
apt-get update
apt-get install expect
apt-get install squid 
apt-get install apache2-utils
cp squid.conf squid.conf.orig
chmod a-w squid.conf.orig
touch /etc/squid3/squid_passwd
chown proxy /etc/squid3/squid_passwd
initctl show-config squid3 
"""
append_conf = os.popen("cat 'Ubuntu Suid Setup Proxy.txt'").readlines()

user = os.popen('users').read().strip(); #get the current user
os.chdir(dir_); # cd directory
list_of_users = []; # initializing list
adduser = ""
pwd = ""
log = "log.log";

while True: # Repeat the process
	client_ip = raw_input("Enter client's IP: ") 
	adduser = raw_input("Client's user: "); # asking for new username
	pwd = raw_input("Client's password: "); # asking for new password
	ask = raw_input("Do you want to add more <Y/n>").strip(); # Asking to continue
	if ask.lower() != 'y': # if ask var is not equal to Y or y
		break
	else: pass

	if ( not adduser or not pwd ): # test if user and or password is not empty
		print "User and or password should not be empty."; # display an error
	else:
		list_of_users.append(([adduser, pwd])); #insert user and password
print list_of_users
sys.exit()

if re.search(" ", user): # check if user have space in between
	user=user.split() # split it by space
	user=user[0] # get user at index zero
else: pass

if os.path.isfile(log): # test if log.log exists
	os.remove(log); # remove log.log file
else: pass

if os.path.isdir(dir_): # test if directory exists
	for i in commands.split('\n'): # split commands
		os.system(i); # execute commands
	if os.path.isfile("%s.conf" % squid):
		write_to_file('log.log', (date_time() + ' %s successfully copied a backup.' % squid))

	os.system("sed -i -e 's/http_access deny all/http_access allow/g' %s" % squid); # find and replace http_access deny all to http_access allow
	outp = os.popen("cat %s |grep 'http_access deny all'").read().strip()
	if outp:
		print '%s not being replace.' % squid
		raw_input('Error here.')
	else:
		pass
	# iterate append_conf
	for i in append_conf.split("\n"):
		check = os.popen("cat %s |grep '%s'" % (squid, i)).read().strip()
		if not check: # if null or empty
			write_to_file(squid, i); # writing into conf file
	os.system("service squid3 restart"); # restart squid
else: 
	print 'Directory %s does not exists!' % dir_;
	sys.exit(); # quit script

