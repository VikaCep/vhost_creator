#!/usr/bin/env python

import os
from io import open

# default values
default_vhosts_file = "/etc/apache2/sites-enabled/000-default.conf"
default_domain = "local"
default_hosts_file = "/etc/hosts"
default_index = "index.php"
default_ipaddress = "127.0.0.1"

#user input
hosts_file = raw_input('Enter the path to the hosts file (default '+default_hosts_file+'): ') or default_hosts_file
vhosts_file = raw_input('Enter the path to the virtual hosts file (default '+default_vhosts_file+'): ') or default_vhosts_file
domain = raw_input ('Enter the domain name (default '+default_domain+'): ') or default_domain
index = raw_input ('Enter the index file (default '+default_index+'): ') or default_index
ipaddress = raw_input ('Enter the ip address (default '+default_ipaddress+'): ') or default_ipaddress
project = raw_input('Enter the name of project (lowercase, no spaces): ')
docroot = raw_input('Enter the path to the public directory of your application: ')

#adding entry to hosts file as project.local
print "Creating new entry in hosts file as ",project
f = open(hosts_file,'a')
entry = "\n" + ipaddress + "\t" + project+"."+domain + "\n"
f.write(unicode(entry))
f.close()

#adding virtualhost code
print "Adding the VirtualHost code in ",vhosts_file
virtualhost="""
<VirtualHost 127.0.0.1>
  DocumentRoot %(docroot)s
  DirectoryIndex %(index)s
  ServerName %(project)s.%(domain)s
  <Directory %(docroot)s>
	 AllowOverride all
	 Order allow,deny
	 Allow from all
	 # New directive needed in Apache 2.4.3: 
	 Require all granted
  </Directory>
</VirtualHost>
"""

f = open(vhosts_file, 'a')
f.write(unicode(virtualhost % dict(project=project, docroot=docroot, domain=domain, index=index)))
f.close()

#restarting apache2 server
print "[notice]\tRestarting Apache Server";
os.system("sudo service apache2 restart")

print "Done! you can now access it from http://"+project+"."+domain;

