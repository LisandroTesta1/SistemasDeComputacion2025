#include <linux/module.h>
#include <linux/version.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/kdev_t.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>

static dev_t first;         // Device number (major + minor)
static struct cdev c_dev;   // Character device structure
static struct class *cl;    // Device class

static int my_open(struct inode *i, struct file *f)
{
    printk(KERN_INFO "Driver3_SdeC: open()\n");
    return 0;
}
static int my_close(struct inode *i, struct file *f)
{
    printk(KERN_INFO "Driver3_SdeC: close()\n");
    return 0;
}
static ssize_t my_read(struct file *f, char __user *buf, size_t len, loff_t *off)
{
    printk(KERN_INFO "Driver3_SdeC: read()\n");
    return 0;
}
static ssize_t my_write(struct file *f, const char __user *buf, size_t len, loff_t *off)
{
    printk(KERN_INFO "Driver3_SdeC: write()\n");
    return len;
}

static struct file_operations pugs_fops =
{
    .owner = THIS_MODULE,
    .open = my_open,
    .release = my_close,
    .read = my_read,
    .write = my_write
};

static int __init drv3_init(void)
{
    int ret;
    struct device *dev_ret;

    printk(KERN_INFO "SdeC_drv3 Registrado exitosamente..!!\n");

    if ((ret = alloc_chrdev_region(&first, 0, 1, "SdeC_drv3")) < 0)
    {
        return ret;
    }

    cl = class_create("chardrv");  // <- ACTUALIZADO para kernels 6.10+
    if (IS_ERR(cl))
    {
        unregister_chrdev_region(first, 1);
        return PTR_ERR(cl);
    }

    dev_ret = device_create(cl, NULL, first, NULL, "SdeC_drv3");
    if (IS_ERR(dev_ret))
    {
        class_destroy(cl);
        unregister_chrdev_region(first, 1);
        return PTR_ERR(dev_ret);
    }

    cdev_init(&c_dev, &pugs_fops);
    if ((ret = cdev_add(&c_dev, first, 1)) < 0)
    {
        device_destroy(cl, first);
        class_destroy(cl);
        unregister_chrdev_region(first, 1);
        return ret;
    }

    return 0;
}

static void __exit drv3_exit(void)
{
    cdev_del(&c_dev);
    device_destroy(cl, first);
    class_destroy(cl);
    unregister_chrdev_region(first, 1);
    printk(KERN_INFO "SdeC_drv3 dice Adios mundo cruel..!!\n");
}

module_init(drv3_init);
module_exit(drv3_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Cátedra Sistemas de Computación");
MODULE_DESCRIPTION("Nuestro tercer driver de SdeC");

