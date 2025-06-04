#include <linux/module.h>
#include <linux/kernel.h>
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Mi primer modulo de ejemplo");
MODULE_AUTHOR("Lisandro Testa");
MODULE_VERSION("1.0");

int modulo_lin_init(void){
    
    printk(KERN_INFO "Modulo cargado en el kernel con exito. \n");

    return 0;
}

void modulo_lin_clean(void){

    printk(KERN_INFO "Modulo descargado del kernel con exito. \n");

}

module_init(modulo_lin_init);
module_exit(modulo_lin_clean);
