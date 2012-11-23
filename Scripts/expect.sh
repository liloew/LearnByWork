#!/usr/bin/expect
# 获取文件锁
set fid [open /home/lilo/secret]
# 由文件获取密码
set password [read $fid]
spawn ftp localhost
expect {
	-re ".*Are.*.*yes.*no.*" {
	send "yes\n"
	exp_continue
	}
	-re ".*Name.*.*:" {
	send "ftp\n"
	exp_continue
	}
	"*?assword:*" {
		send $password
		send "\n"
	#	interact
		exp_continue
		}
	"ftp> " {
	send "get eula.en_US"
	send "\n"
	interact
	}
}
