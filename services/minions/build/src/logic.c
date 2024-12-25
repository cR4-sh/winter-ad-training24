#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <banners.h>
#include <minions.h>

void logic() {
    puts(WELCOME);

    char command[8] = {0};
    while (1) {
        puts(MENU);
        printf(" [MINIONS] Enter command: ");

        if (fgets(command, sizeof(command), stdin) == NULL) {
            puts(" [ERROR] Failed to get command!");
            return;
        }

        size_t index = strcspn(command, "\n");
        if (index > 2) {
            puts(" [ERROR] Command is too big!");
            return;
        }
        command[index] = 0;
        
        int command_ = strtol(command, NULL, 10);
        switch (command_){
            case 1: {
                registerMinion();
                break;
            }
            case 2: {
                loginMinion();
                break;
            }
            case 3: {
                showMyMinion();
                break;
            }
            case 4: {
                createFamily();
                break;
            }
            case 5: {
                joinFamily();
                break;
            }
            case 6: {
                familyInfo();
                break;
            }
            case 7: {
                familyMinionInfo();
                break;
            }
            case 8: {
                logout();
                break;
            }
            case 9: {
                puts(" [MINIONS] See you later!");
                return;
            }
            case -9: {
                gruDoor();
                break;
            }
            default: {
                puts(" [ERROR] Invalid command!");
            }
        }        
    }
}