# Practice: Consistency exercise
## Design a mechanism for supporting consistency when you write a file
- Assume you update a file whose size is 10KB → 3 disk blocks
- How to guarantee that all 3 blocks are written or not
- Candidates
    - fsync after each write
    - employ transaction
    - make use of counting semaphore (or concurrency mechanism)
    - …
```C
#include <stdio.h>
…
#define MAX_BUF 4096

int main(int argc, char *argv[])
{
	…
	while (1) {
		…
		// prepare data
		…
		write_size = write(fd, buf, MAX_BUF);
	}
	…
}
```
