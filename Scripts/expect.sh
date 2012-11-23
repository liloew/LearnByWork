#!/usr/bin/expect
set fid [open /root/secret]
set password [read $fid]
spawn ssh localhost
expect {
	-re ".*Are.*.*yes.*no.*" {
	send "yes\n"
	exp_continue
	}
	"*?assword:*" {
		send $password
		send "\n"
		interact
		}
}
