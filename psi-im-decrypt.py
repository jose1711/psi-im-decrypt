#!/usr/bin/env python
"""
decrypts stored passwords used by Psi messenger
(psi-im.org)

the idea is from
https://www.georglutz.de/blog/2005/07/01/recover-lost-jabber-passwords-in-psis-config-files/

Copyright © 2019 Jose Riha <jose1711 gmail com>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See http://www.wtfpl.net/ for more details.

"""
import xml.etree.ElementTree as ET
import argparse
from itertools import cycle

description = '''
Decrypt passwords from accounts.xml file
provided as an argument. Account jids and
passwords are sent to stdout.

Example:
%(prog)s ~/.config/psi/profiles/default/accounts.xml
'''

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('accounts_file', nargs=1, help='path to accounts.xml file')
args = parser.parse_args()

tree = ET.parse(args.accounts_file[0])
root = tree.getroot()

ns = {'psi': 'http://psi-im.org/options'}

def decodePassword(password, jid):
    result = ''
    jid = cycle(jid)
    for n1 in range(0, len(password), 4):
        x = int(password[n1:n1+4], 16)
        result += chr(x ^ ord(next(jid)))
    return result

for el in root.findall('.//*/psi:password/..', ns):
    try:
        password = el.find('./psi:password', ns).text
        jid = el.find('./psi:jid', ns).text
    except AttributeError:
        continue
    print(jid, decodePassword(password, jid))
