#include <gba.h>
#include <stdio.h>
#include <stdlib.h>

#include "imageData.h"
#include "graphics.h"

int main(void) {
    
    initGraphics();
    initText(NULL);

    setSpritePriority(0, 2);
    setSpriteEnable(0);

    printText("Hello my very dear world. adwdawd awd awd awdawdawd awdawdceagvar bvarb awebvwea fwe f aewdb vas dvew sdv asg avra sdbv vasdb vaesb awdgrab rebsv sg varsbv ws bv rsdbv sd bvaa sbdvaa wesvd");

    int herox = 0;
    int heroy = 0;

    int herospeed = 1;

    while (true) {
        VBlankIntrWait();
        scanKeys();
        int kd = keysDown();
        if (keysHeld() & KEY_RIGHT) {
            herox += herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_LEFT) {
            herox -= herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_UP) {
            heroy -= herospeed;
            moveHero(&herox, &heroy);
        }
        if (keysHeld() & KEY_DOWN) {
            heroy += herospeed;
            moveHero(&herox, &heroy);
        }
        if (kd & KEY_A) {
            printText("SUBSCRIBE TO PEWDIEPIE! ");
        }
        if (kd & KEY_B) {
            clearSpriteGraphics();
        }
    }
}
