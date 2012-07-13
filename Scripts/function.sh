#!/bin/bash
################################################################################
#
#	Author	 :lilo
#	Version  :2.1
#	Date	 :2012-07-07
#	Copyright:金智教育 www.wisedu.com
#
################################################################################
LOG=/var/log/Nagios-plugin-install-`date +%Y%m%d%H%M%S`.log
export LOG
function apache(){
	wget -c ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.30.tar.bz2
	tar xvf pcre-8.30.tar.bz2 && cd pcre-8.30
	./configure --prefix=/usr/local/pcre 2>&1 | tee $LOG
	make 2>&1 | tee $LOG
	make install 2>&1 | tee $LOG
	cd -
	echo "Install apache---------------------------------"
	wget -c http://mirror.bjtu.edu.cn/apache//httpd/httpd-2.4.2.tar.bz2
	tar xvf httpd-2.4.2.tar.bz2 && cd httpd-2.4.2
	wget -c http://labs.mop.com/apache-mirror//apr/apr-1.4.6.tar.bz2
	tar xvf apr-1.4.6.tar.bz2 -C srclib/
	mv srclib/apr-1.4.6/ srclib/apr
	wget -c http://labs.mop.com/apache-mirror//apr/apr-util-1.4.1.tar.bz2
	tar xvf apr-util-1.4.1.tar.bz2 -C srclib/
	mv srclib/apr-util-1.4.1 srclib/apr-util
	./configure --prefix=/usr/local/apache2 --with-included-apr --with-mpm=worker --enable-deflate --enable-cache --enable-disk-cache --enable-file-cache --enable-mem-cache --enable-rewrite --enable-so --enable-speling --enable-ssl --with-apr --with-apr-util --with-ssl --with-z --enable-modules=all --with-pcre=/usr/local/pcre --enable-mods-shared=all 2>&1 | tee $LOG
	make all 2>&1 | tee $LOG
	make install 2>&1 | tee $LOG
	echo "Modified httpd.conf"
	sed -ie "/DirectoryIndex index.htm/s/$/ index.php/" /usr/local/apache2/conf/httpd.conf
	sed -ie "s/#LoadModule rewrite_module modules/LoadModule rewrite_module modules/g" /usr/local/apache2/conf/httpd.conf
	sed -ie "s/#LoadModule cgid_module modules/LoadModule cgid_module modules/g" /usr/local/apache2/conf/httpd.conf
	/usr/local/apache2/bin/apachectl -t 1>/dev/null 2>&1
	if [[ $? == 0 && `ps aux | grep -c http` -lt 2 ]]
	then
		/usr/local/apache2/bin/apachectl start
		echo "httpd has been started"
	else
		echo "Httpd has been started"
		echo "Please check and run $0 mysql"
		exit 2
		#return 2
	fi
	echo "/usr/local/apache2/bin/apachectl start" >> /etc/rc.local
	cd -
}

function mysql(){
	rpm -ivh MySQL-client-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-client Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh MySQL-server-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-server Error" 2>&1 | tee $LOG
		exit 1
	fi
	/etc/init.d/mysql start 2>&1 | tee $LOG
	sleep 15
	mysqladmin -u root password 'wiscom123' 2>&1 | tee $LOG
	rpm -ivh MySQL-devel-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-devel Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh MySQL-shared-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-shared Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh MySQL-shared-compat-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-shared-compat Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh MySQL-test-5.5.25-1.rhel5.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install MySQL-test Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh perl-DBI-1.620-1.el5.rfx.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install perl-DBI Error" 2>&1 | tee $LOG
		exit 1
	fi
	rpm -ivh perl-DBD-MySQL-4.014-1.el5.rfx.x86_64.rpm 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install perl-DBD Error" 2>&1 | tee $LOG
		exit 1
	fi
}

function zlib(){
	wget -c http://www.imagemagick.org/download/delegates/zlib-1.2.7.tar.bz2
	tar xvf zlib-1.2.7.tar.bz2 && cd zlib-1.2.7
	./configure --prefix=/usr/local/zlib 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config zlib Error!" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make zlib Error" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install zlib Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -
}
function jpeg(){
	wget -c http://nchc.dl.sourceforge.net/project/libjpeg/libjpeg/6b/jpegsr6.zip
	unzip jpegsr6.zip
	mkdir -pv /usr/local/jpeg6/{include,lib,bin,man{,/man1}}
	if [[ "$?" != 0 ]]; then
		echo "mkdir for jpegsr Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd jpeg-6b/
	dos2unix configure
	if [[ "$?" != 0 ]]; then
		echo "Format config for jpegsr Error" 2>&1 | tee $LOG
		exit 1
	fi
	./configure --prefix=/usr/local/jpeg6 --enable-shared --enable-static 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config jpegsr Error" 2>&1 | tee $LOG
		exit 1
	fi
	sed -ie "s:./libtool:/usr/bin/libtool:g" Makefile
	if [[ "$?" != 0 ]]; then
		echo "sed Makefiel Error" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make jpegsr Error" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install jpegsr Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -
}
function libpng(){
	wget -c http://nchc.dl.sourceforge.net/project/libpng/libpng15/older-releases/1.5.10/libpng-1.5.10.tar.bz2
	tar xvf libpng-1.5.10.tar.bz2 && cd libpng-1.5.10
	./configure --prefix=/usr/local/libpng 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config libpng Error" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make libpng Error" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install libpng Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -
}
function freetype(){	
	wget -c http://nchc.dl.sourceforge.net/project/freetype/freetype2/2.4.9/freetype-2.4.9.tar.bz2
	tar xvf freetype-2.4.9.tar.bz2 && cd freetype-2.4.9
	./configure --prefix=/usr/local/freetype2 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config freetype Error" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make freetype Error" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Install freetype Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -
}
function gd(){
	wget -c http://fossies.org/unix/www/gd-2.0.35.tar.gz	# 1
	tar xvf gd-2.0.35.tar.gz && cd gd-2.0.35		# 2
	./configure --with-freetype=/usr/local/freetype2 --with-fontconfig=/usr/local --with-jpeg=/usr/local/jpeg6 --with-png=/usr/local/libpng --no-recursion --prefix=/usr/local/gd 2>&1 | tee $LOG				# 3
	if [[ "$?" != 0 ]]; then
		echo "Config gd Error" 2>&1 | tee $LOG
		exit 1
	fi
	make clean
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make gd Error" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG				# 5
	if [[ "$?" != 0 ]]; then
		echo "Install gd Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -							# 6
}

function php(){
	wget -c http://cn.php.net/distributions/php-5.3.14.tar.bz2
	tar xvf php-5.3.14.tar.bz2 && cd php-5.3.14
	./configure --prefix=/usr/local/php \
	--with-apxs2=/usr/local/apache2/bin/apxs \
	--with-config-file-path=/usr/local/php \
	--with-mysqli=/usr/bin/mysql_config \
	--with-gd=/usr/local/gd \
	--with-jpeg-dir=/usr/local/jpeg6 \
	--with-png-dir=/usr/local/libpng \
	--with-zlib-dir=/usr/local/zlib \
	--with-freetype-dir=/usr/local/freetype2 \
	--enable-ftp \
	--enable-zip \
	--enable-gd-native-ttf \
	--enable-gd-jis-conv \
	--with-curl \
	--enable-sqlite-utf8 \
	--enable-sockets 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config php Error!" 2>&1 | tee $LOG
	fi
	make all 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make php Error!" 2>&1 | tee $LOG
	fi
	#make test
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]
	then
		echo "Make Install php Error!" 2>&1 | tee $LOG
		exit 1
	fi
	sed -ie '/AddType application\/x-compress .Z/a\AddType application\/x-httpd-php .php' /usr/local/apache2/conf/httpd.conf
	cp php.ini-development /usr/local/lib/php.ini
	/usr/local/apache2/bin/apachectl -t 1>/dev/null 2>&1
	if [[ "$?" == 0 && `ps aux | grep -c http` -gt 2 ]]
	then
		/usr/local/apache2/bin/apachectl stop
		sleep 2
		/usr/local/apache2/bin/apachectl start
		if [[ "$?" != 0 ]]; then
			echo "httpd doesn't work" 2>&1 | tee $LOG
			exit 2
		fi
		echo "httpd has been started" 2>&1 | tee $LOG
	else
		echo "httpd.conf has some errors" 2>&1 | tee $LOG
		exit 2
	fi
	cat > /usr/local/apache2/htdocs/p.php << EOF
<?
	phpinfo();
?>
EOF
	echo "Please test:http://<ip>/p.php"
	return 0
}

function nagios(){
	mkdir -pv /etc/httpd/conf.d/
	if [[ "$?" != 0 ]]; then
		echo "mkdir Error" 2>&1 | tee $LOG
		exit 1
	fi
	wget -c http://nchc.dl.sourceforge.net/project/nagios-cn/sourcecode/zh_CN%203.2.3/nagios-cn-3.2.3.tar.bz2
	tar xvf nagios-cn-3.2.3.tar.bz2 && cd nagios-cn-3.2.3
	./configure --with-command-user=nagios --with-command-group=nagios --prefix=/usr/local/nagios 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config Error!" 2>&1 | tee $LOG
		exit 1
	fi
	make all 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make Error!" 2>&1 | tee $LOG
		exit 1
	fi
	if [ `grep nagios /etc/passwd | cut -d: -f 1` ]
	then
		echo "===========================user nagios exist=============================" 2>&1 | tee $LOG
	else
		echo "============================Add user nagios==============================" 2>&1 | tee $LOG
		#useradd -s /sbin/nologin nagios
		useradd -s /bin/bash nagios
	fi
	make install 2>&1 | tee $LOG
	make install-init 2>&1 | tee $LOG
	make install-config 2>&1 | tee $LOG
	make install-commandmode 2>&1 | tee $LOG
	make install-webconf 2>&1 | tee $LOG
	chkconfig --add nagios
	chkconfig nagios on
	#chown -R nagios:nagios /usr/local/nagios
	/etc/init.d/nagios start
	echo "Include /etc/httpd/conf.d/*.conf" >> /usr/local/apache2/conf/httpd.conf
	/usr/local/apache2/bin/apachectl -t 1>/dev/null 2>&1
	if [[ $? == 0 && `ps aux | grep -c http` -gt 2 ]]
	then
		/usr/local/apache2/bin/apachectl stop
		sleep 2
		/usr/local/apache2/bin/apachectl start
		if [[ "$?" != 0 ]]; then
			echo "httpd doesn't work" 2>&1 | tee $LOG
			echo "Please chechk,and run $0 nagios-plungin" 2>&1 | tee $LOG
			exit 2
		fi
		echo "httpd has been started" 2>&1 | tee $LOG
	else
		echo "httpd.conf has some errors" 2>&1 | tee $LOG
		exit 2
	fi
}

function nagios-plugin(){
	wget -c http://nchc.dl.sourceforge.net/project/nagiosplug/nagiosplug/1.4.16/nagios-plugins-1.4.16.tar.gz
	tar xvf nagios-plugins-1.4.16.tar.gz && cd nagios-plugins-1.4.16
	echo "======================Configure Nagios-plugin========================"
	./configure --prefix=/usr/local/nagios --without-mysql --with-nagios-user=nagios --with-nagios-group=nagios 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]
	then
        	echo "=============================Config Error================================" 2>&1 | tee $LOG
        	exit 1
	fi
	echo  "=======================Compile Nagios plugin=========================" 2>&1 | tee $LOG
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make nagios-plugin Error" 2>&1 | tee $LOG
		exit 1
	fi
	echo  "=======================Install Nagios plugin=========================" 2>&1 | tee $LOG
	make install 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make Install nagios-plugin Error!" 2>&1 | tee $LOG
		exit 2
	fi
	service nagios restart
	/usr/local/apache2/bin/apachectl restart
}

function nrpe(){
	# Check root user
	if [ $(id -u) != "0" ]; then
    	echo "[Error]: You must be root to run this script, please use root to install script" 2>&1 | tee $LOG
    	echo "[Error]: You must be root to run this script, please use root to install script"
    	exit 1
	fi
	
	# Keep in the source directory
	if [ "$1" == "" ]
	then
        	echo "=============================Current Directory===========================" 2>&1 | tee $LOG 
			echo "`pwd`"
	else
        	cd $1
        	echo "`pwd`"
	fi
	#Disable SeLinux
	echo "=============================Disable SELinux=============================" 2>&1 | tee $LOG
	echo "=============================Disable SELinux============================="
	if [ -s /etc/selinux/config ]; then
		cp /etc/selinux/config /etc/selinux/config-`date +%Y%m%d%H%M%S`.bak
		sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
	fi
	echo "==========================check OpenSSL and OpenSSL-devel================" 2>&1 | tee $LOG
	OPENSSL=`rpm -qa | grep -i openssl-devel`
	if [ -z `echo $OPENSSL | cut -d" " -f1` ]
	then
		echo "=====================OpenSSL Devel not installed=========================" 2>&1 | tee $LOG
		bash ./openssl-devel.sh
		STAT=$?
		if [[ "$STAT" != 0 ]]
		then
			echo "=====================OpenSSL Devel not installed=========================" 2>&1 | tee $LOG
			echo "=====================OpenSSL Devel not installed========================="
		fi
	else
		echo "======================OpenSSL Devel Installed==========================" 2>&1 | tee $LOG
	fi
	#SSL=`find / -name "libssl.so*" -type f`
	#if [ -z `echo $SSL | cut -d" " -f1` ]
	#then
	#	echo "====================OpenSSL Devel not installed========================"
	#else
	#	ln -sv `echo $SSL | cut -d" " -f1` /usr/lib/libssl.so
	#fi
	echo "========================================================================="
	if [ `grep nagios /etc/passwd | cut -d: -f 1` ]
	then
		echo "===========================user nagios exist=============================" 2>&1 | tee $LOG
	else
		echo "============================Add user nagios==============================" 2>&1 | tee $LOG
		/usr/sbin/useradd -s /sbin/nologin nagios
	fi
	wget -c http://nchc.dl.sourceforge.net/project/nagios/nrpe-2.x/nrpe-2.13/nrpe-2.13.tar.gz
	tar xvf nrpe-2.13.tar.gz && cd nrpe-2.13
	echo "==================================Compile NRPE==========================="
	./configure --prefix=$INSTDIR --with-nagios-user=nagios --with-nagios-group=nagios 2>&1 | tee $LOG
	#STAT=$?
	#echo $STAT
	if [[ "$?" != 0 ]]
	then
		echo "==================================Compile Error===========================" 2>&1 | tee $LOG
		echo -e "=================================\033[1mCompile Error\033[0m==========================="
		exit 1
	fi
	echo "==================================Make NRPE==============================" 2>&1 | tee $LOG
	make all 2>&1 | tee $LOG
	if [ $? == 0 ]
	then 
		echo "===========================Successfully Make NRPE=============================" 2>&1 | tee $LOG
	else
		echo "===============================Make NRPE [Error]================================" 2>&1 | tee $LOG
	fi
	echo "===============================Install NRPE==============================" 2>&1 | tee $LOG
	make install-plugin 2>&1 | tee $LOG
	make install-daemon 2>&1 | tee $LOG
	make install-daemon-config 2>&1 | tee $LOG
	make install-xinetd 2>&1 | tee $LOG
	chown nagios:nagios /usr/local/nagios
	chown -R nagios:nagios /usr/local/nagios/libexec
	cp /etc/services /etc/services.bak-`date +%Y%m%d%H$M%S`
	echo "nrpe            5666/tcp                        # NRPE" >> /etc/services
	echo "========================Successfully Installed NRPE===========================" 2>&1 | tee $LOG
	retunr 0
}

function ndoutils(){
	function judge() {
		echo "============================================================================"
		echo "You must run soome commands bleow:"
		echo "mysql -u root -p	# you mysql password"
		echo "create database nagios;"
		echo "grant all privileges on nagios.* to nagios@localhost identified by 'nagios';"
		echo "flush privileges;"
		echo "quit"
		read -p "Do you complete run these commands?[y|n]" var
		echo "============================================================================"
		if [[ "$var" == "n" ]]; then
			echo "You should complete those commands"
			judge
		fi
		return 0
	}
	NAGUSER=nagios			#the user nagios
	NAGGROUP=nagios			#the user nagios group
	NAGPASSWD=nagios		#the database user password
	NAGDATABASE=nagios		#the database name
	wget -c http://nchc.dl.sourceforge.net/project/nagios/ndoutils-1.x/ndoutils-1.5.1/ndoutils-1.5.1.tar.gz
	tar xvf ndoutils-1.5.1.tar.gz && cd ndoutils-1.5.1
	./configure --prefix=/usr/local/nagios --enable-mysql 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Config ndoutils Error" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make ndoutils Error" 2>&1 | tee $LOG
		exit 1
	fi
	judge
	cd db/
	./installdb -u $NAGUSER -p $NAGPASSWD -h localhost -d $NAGDATABASE 2>&1 | tee $LOG
	#if [ `./installdb -u $NAGUSER -p $NAGPASSWD -h localhost -d $NAGDATABASW | cut -d" " -f3` == "already" ]; then
	#	./upgradedb -u $NAGUSER -p $NAGPASSWD -h localhost -d $NAGDATABASE
	#fi
	if [[ "$?" != 0 ]]; then
		echo "installde or upgradedb Error" 2>&1 | tee $LOG
		exit 1
	fi
	cd -
	cp src/ndo2db-3x src/ndomod-3x.o src/log2ndo /usr/local/nagios/bin
	cp config/ndo2db.cfg-sample /usr/local/nagios/etc/ndo2db.cfg
	cp config/ndomod.cfg-sample /usr/local/nagios/etc/ndomod.cfg
	echo "broker_module=/usr/local/nagios/bin/ndomod-3x.o config_file=/usr/local/nagios/etc/ndomod.cfg" >> /usr/local/nagios/etc/nagios.cfg
	sed -i "s/db_user=ndouser/db_user=$NAGUSER/g" /usr/local/nagios/etc/ndo2db.cfg
	sed -i "s/ndo2db_group=nagios/ndo2db_group=$NAGGROUP/g" /usr/local/nagios/etc/ndo2db.cfg
	sed -i "s/db_pass=ndopassword/db_pass=$NAGPASSWD/g" /usr/local/nagios/etc/ndo2db.cfg
	sed -i "s/db_name=nagios/db_name=$NAGDATABASE/g" /usr/local/nagios/etc/ndo2db.cfg
	chown -R nagios:nagios /usr/local/nagios/
	/usr/local/nagios/bin/ndo2db-3x -c /usr/local/nagios/etc/ndo2db.cfg
	cp /etc/rc.local /etc/rc.local-`date +%Y%m%d%H%M%S`.bak
	echo "/usr/local/nagios/bin/ndo2db-3x -c /usr/local/nagios/etc/ndo2db.cfg" >> /etc/rc.local
	/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg 1>/dev/null 2>&1
	if [[ "$?" != 0 ]]; then
		echo "nagios.cfg file exists error" 2>&1 | tee $LOG
		echo "nagios server not start" 2>&1 | tee $LOG
		exit 1
	fi
	/etc/init.d/nagios stop
	sleep 2
	/etc/init.d/nagios start
}

function rrdtool(){
	wget -c http://ftp.acc.umu.se/pub/gnome/sources/libart_lgpl/2.3/libart_lgpl-2.3.17.tar.gz
	tar xvf libart_lgpl-2.3.17.tar.gz && cd libart_lgpl-2.3.17
	./configure --disable-shared 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Configu Error!" 2>&1 | tee $LOG
		exit 1
	fi
	make 2>&1 | tee $LOG
	if [[ "$?" != 0 ]]; then
		echo "Make Error!" 2>&1 | tee $LOG
		exit 1
	fi
	make install 2>&1 | tee $LOG
	
	wget -c http://fossies.org/unix/misc/rrdtool-1.4.7.tar.gz
	tar xvf rrdtool-1.4.7.tar.gz
	cd rrdtool-1.4.7
	./configure --prefix=/usr/local/rrdtool --disable-python --disable-tcl 2>&1 | tee $LOG
	make 2>&1 | tee $LOG
	make install 2>&1 | tee $LOG
	cd -
}
function pnp4nagios(){	
	wget -c http://ncu.dl.sourceforge.net/project/pnp4nagios/PNP-0.6/pnp4nagios-0.6.17.tar.gz
	tar xvf pnp4nagios-0.6.17.tar.gz && cd pnp4nagios-0.6.17
	./configure --with-rrdtool=/usr/local/rrdtool/bin/rrdtool --with-nagios-user=nagios --with-nagios-group=nagios 2>&1 | tee $LOG
	make all 2>&1 | tee $LOG
	make fullinstall 2>&1 | tee $LOG
	echo "broker_module=/usr/local/pnp4nagios/lib/npcdmod.o config_file=/usr/local/pnp4nagios/etc/npcd.cfg" >> /usr/local/nagios/etc/nagios.cfg
	/usr/local/pnp4nagios/bin/npcd -d -f /usr/local/pnp4nagios/etc/npcd.cfg
	cp /etc/rc.local /etc/rc.local-`date +%Y%m%d%H%M%S`.bak
	echo "/usr/local/pnp4nagios/bin/npcd -d -f /usr/local/pnp4nagios/etc/npcd.cfg" >> /etc/rc.local
	/usr/local/apache2/bin/apachectl -t 1>/dev/null 2>&1
	if [[ $? == 0 && `ps aux | grep -c http` -gt 2 ]]
	then
		/usr/local/apache2/bin/apachectl stop
		sleep 2
		/usr/local/apache2/bin/apachectl start
		if [[ "$?" != 0 ]]; then
			echo "httpd doesn't work" 2>&1 | tee $LOG
			exit 2
		fi
		echo "httpd has been started" 2>&1 | tee $LOG
	else
		echo "httpd.conf has some errors" 2>&1 | tee $LOG
		exit 2
	fi
	echo "Please visit:http://<ip>/pnp4nagios to test" 2>&1 | tee $LOG
	read -p "Please input one username to access the:http://<ip>/nagios and http://<ip>/pnp4nagios :" NAGUSERNAME
	read -p "Please input password:" NAGPASSWD
	/usr/local/apache2/bin/htpasswd -cb /usr/local/nagios/etc/htpasswd.users $NAGUSERNAME $NAGPASSWD
}
case "$1" in
	apache)
		apache
		mysql
		zlib
		jpeg
		libpng
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	mysql)
		mysql
		zlib
		jpeg
		libpng
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	zlib)
		zlib
		jpeg
		libpng
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	jpeg)
		jpeg
		libpng
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	libpng)
		libpng
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	freetype)
		freetype
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	gd)
		gd
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	php)
		php
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	nagios)
		nagios
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	nagios-plugin)
		nagios-plugin
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	nrpe)
		nrpe
		ndoutils
		rrdtool
		pnp4nagios
		;;
	ndoutils)
		ndoutils
		rrdtool
		pnp4nagios
		;;
	rrdtool)
		rrdtool
		pnp4nagios
		;;
	pnp4nagios)
		pnp4nagios
		;;
	*)
		echo $"Usage: $0 {apache|mysql|zlib|jpeg|libpng|freetype|gd|php|nagios|nagios-plugin|nrpe|ndoutils|rrdtool|pnp4nagios}"
esac
echo "Please modified /etc/xinet.d/nrpe" | tee $LOG
exit $?

