#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h> 
#include <semaphore.h>
#include <string.h>
#include <errno.h>

#define MAX_BUF 4096

sem_t semaphore;

int main(int argc, char *argv[])
{
	int fd, write_size;
	char buf[MAX_BUF];
	char *path = argv[1];
	int size = atoi(argv[2]) * 1024;
	int total_size = 0;

	sem_init(&semaphore, 0, 2);
	
	fd = open(path, O_RDWR|O_SYNC|O_CREAT, 0666);
        if (fd < 0) {
                printf("Failed to open %s\n", path);
                return fd;
        }

	
	sem_wait(&semaphore);

	while(1) {
		write_size = write(fd, buf, MAX_BUF);
		total_size += write_size;
		
		printf("%d, %d / %d \n", write_size, total_size, size);

		if (fsync(fd) == -1) {
			fprintf(stderr, "File Sync Error: %s\n", strerror(errno));
			sem_post(&semaphore);
			return -1;
		}

		if (total_size >= size) {
			sem_post(&semaphore);
			break;
		}
	}
	
	sem_post(&semaphore);
	return 0;
}
