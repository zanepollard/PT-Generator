import pysftp
import paramiko
import os
from base64 import decodebytes

SFTPuser = "cgssftpuser"
SFTPpass = "R3BrxpAu49uCsTllAGyl"
hostname = "3.214.118.213"
keydata = b"AAAAB3NzaC1yc2EAAAABIwAAAIEAlDUKlhnRT0qXfescAJe25L7eTQTm+hgN40+yXWvx3aZuejxMtsobCReKgXsalkuzGJ4LJoG61MpyHUp/JDkrL9DgFtW9jFS3+4NDLEhvi0ieDGLFjHlzEJ5jZJmW6uHb1B3E/auh3iDK7iO5jPxfb98qy5tfhg0//UbZasA7FEU="
key = paramiko.RSAKey(data=decodebytes(keydata))
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add(hostname, 'ssh-rsa', key)

with pysftp.Connection(hostname, username=SFTPuser, password=SFTPpass, cnopts=cnopts) as sftp:
    sftp.put('Test.ignore',preserve_mtime=True)