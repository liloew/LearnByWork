#!/usr/bin/env python
# coding: utf-8
import sys
import pexpect

child = pexpect.spawn('ssh root@173.16.212.128')	# Remote host IP
flog = file('ssh.log','w')
child.logfile = flog
child.expect('yes/no')
child.send('yes\n')
child.expect('assword:')
# child.waitnoecho()
child.setecho(False)
child.send('RemotehostPassword\n')
# child.expect('%')
child.setecho(True)
child.send('ssh-keygen -t rsa\n')
child.expect('Enter file in')
# child.send('\n')
child.send('/root/.ssh/id_rsa\n')
child.expect('Overwrite') 
# 当已经配置好认证关系时，如不覆盖会出错
# child.send('n\n')
child.send('y\n')
# 该两行是键入ssh密钥的密码组，直接两次回车即可
child.expect('Enter passphrase')
child.send('\n')
child.expect('Enter same passphrase')
child.send('\n')
child.send('ssh-copy-id -i ~/.ssh/id_rsa.pub root@173.16.212.1\n')	# Local host IP
child.expect('yes/no')
child.send('yes\n')
child.expect('password:')
# child.waitnoecho()
child.setecho(False)
child.send('LocalhostPassword\n')
child.setecho(True)
child.sendeof()
