#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

#define MAX_BUF 64
#define TASK_COUNT 100

void target_job(int loopsize)
{
        for(int i = 0; i < loopsize; i++);
}

struct timeval measure_time(int count) {
        struct timeval stime, etime, gap;

        gettimeofday(&stime, NULL);
        target_job(count);
        gettimeofday(&etime, NULL);

        gap.tv_sec = etime.tv_sec - stime.tv_sec;
        gap.tv_usec = etime.tv_usec - stime.tv_usec;

        if (gap.tv_usec < 0) {
                gap.tv_sec = gap.tv_sec - 1;
                gap.tv_usec = gap.tv_usec + 1000000;
        }

        // printf("Elapsed time %ldsec :%ldusec\n", gap.tv_sec, gap.tv_usec);

        return gap;
}

int main(int argc, char *argv[])
{
        int fd, read_size, write_size;
        struct timeval time_rec;
        long total_sec, total_usec;
        char buf[MAX_BUF];
        int loops[] = {10000, 100000, 1000000, 10000000, 100000000};

        total_sec = 0;
        total_usec = 0;
        for (int i = 0; i < 5; i ++) {
                for (int j = 0; j < TASK_COUNT; j++) {
                        time_rec = measure_time(loops[i]);
                        total_sec += time_rec.tv_sec;
                        total_usec += time_rec.tv_usec;
                }

                printf("%d loops\n", loops[i]);
                printf("average time : %ld.%06lds\n\n", total_sec/TASK_COUNT, total_usec/TASK_COUNT);
        }
}
