#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
//#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFERSIZE 1024
#define err_sys(x) { perror(x); exit(1); }

int oneToOne(char *sour, char *dest);

int main(int argc, char *argv[]){

	unsigned char i,sl,dl;	// sl = source length; dl = dest length
	char *path1 = "/root/";
	char *path2 = "/var/test/";
	int len1 = strlen(path1);
	int len2 = strlen(path2);
	struct dirent *dd;	//DirectoryDescribe
	DIR *dir;
	char sourcePath[255], destPath[255];

	dir = opendir(path1);

	strcat(sourcePath, path1);
	strcat(destPath, path2);
	/*
	for (i=0; i <= strlen(path1); i++)
		sourcePath[i] = path1[i];
	sourcePath[i-1] = '/';
	sourcePath[i] = '\0';
	printf("Source Path:%s\n", sourcePath);
	sl = i;
	for (i=0; i <= strlen(path2); i++)
		destPath[i] = path2[i];
	destPath[i-1] = '/';
	destPath[i] = '\0';
	*/
	//dl = i;

	while((dd = readdir(dir)) != NULL){
		//printf("d_name: %s\n",dd->d_name);
		if (dd->d_type == 8){
			//printf("d_name: %s\t%d\n",dd->d_name,dd->d_type);
			sourcePath[len1] = '\0';
			destPath[len2] = '\0';
			strcat(sourcePath, dd->d_name);
			strcat(destPath, dd->d_name);
			/*
			for (i = 1; i <= strlen(dd->d_name); i++)
			{
				sourcePath[sl + i - 1 ] = dd->d_name[i-1];
				destPath[dl + i - 1 ] = dd->d_name[i-1];
			}
			printf("d->d_type:%d\n", dd->d_type);
			printf("Now wer are copying file:%s to %s\n", sourcePath, destPath);
			*/
			printf("We are copy file:%s to %s\n", sourcePath, destPath);
			oneToOne(sourcePath,destPath);
		}
	}

	closedir(dir);
	exit(0);
}

int oneToOne(char *sour, char *dest){
	
	//FILE *s = fopen(sour,"r");
	//FILE *d = fopen(dest,"w");
	ssize_t n;
	int s;
	int d;
	char buf[BUFFERSIZE];

	if( (s = open(sour, O_RDONLY)) <= 0 ){
		err_sys("Open Read error")
		return 1;
	}
	if ( (d = open(dest, O_CREAT|O_WRONLY, S_IRWXU|S_IRGRP|S_IXGRP|S_IROTH|S_IXOTH)) <= 0 ){
		err_sys("Open Write error!");
		return 1;
	}
	//printf("file description:\t%d\t%d\n",s,d);
	while ((n = read(s, buf, BUFFERSIZE)) > 0){ 
		if (write(d, buf, n) != n){
			err_sys("Write error");
			//return 1;
			break;
		}
	//	printf("%s\n",buf);
	}

	if (n < 0)
		err_sys("Read error");
	//exit(0);
	close(s);
	close(d);
	return 0;
}
