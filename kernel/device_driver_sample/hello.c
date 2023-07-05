#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/module.h>

MODULE_DESCRIPTION("Sample Kernel Module");
MODULE_AUTHOR("imdy1207");
MODULE_VERSION("1.0.0");
MODULE_LICENSE("GPL");

static int sample_init(void)
{
	printk(KERN_DEBUG "Hi~!\n");
	return 0;
}

static void sample_exit(void)
{
	printk(KERN_DEBUG "Bye~!\n");
}

module_init(sample_init);
module_exit(sample_exit);
