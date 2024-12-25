#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#include <banners.h>
#include <minions.h>
#include <utils.h>

struct Minion* loggedInMinion = NULL; 

void registerMinion() {
    if (loggedInMinion != NULL) {
        puts(" [ERROR] Minion is already logged in!");
        return;
    }

    char name[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minions name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    name[strcspn(name, "\n")] = 0;

    if (!strlen(name)) {
        puts(" [ERROR] Invalid minion's name!");
        return;
    }

    if (checkMinionExists(name)) {
        puts(" [ERROR] Minion already registered!");
        return;
    }
    
    if (strstr(name, "..") != NULL || strstr(name, "/") != NULL) {
        puts(" [ERROR] Invalid minion's name!");
        return;
    }

    char password[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minions password: ");
    if (fgets(password, sizeof(password), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    password[strcspn(password, "\n")] = 0;
    if (!strlen(password)) {
        puts(" [ERROR] Invalid minion's password!");
        return;
    }

    char secret[BIG_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minions secret: ");
    if (fgets(secret, BIG_DEFAULT_STRLEN, stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    secret[strcspn(secret, "\n")] = 0;

    struct Minion* minion = calloc(1, sizeof(struct Minion));
    strcpy(minion->name, name);
    strcpy(minion->password, password);
    strcpy(minion->secret, secret);

    saveMinion(minion);

    free(minion);
    puts(" [MINIONS] Minion successfully registered!");
    return;
}

void loginMinion() {
    if (loggedInMinion != NULL) {
        puts(" [ERROR] Minion is already logged in!");
        return;
    }

    char name[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minions name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    name[strcspn(name, "\n")] = 0;
    if (!strlen(name)) {
        puts(" [ERROR] Invalid minion's name!");
        return;
    }

    if (!checkMinionExists(name)) {
        puts(" [ERROR] No such minion!");
        return;
    }

    char password[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minions password: ");
    if (fgets(password, sizeof(password), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    password[strcspn(password, "\n")] = 0;

    if (!strlen(password)) {
        puts(" [ERROR] Invalid minion's password!");
        return;
    }
    
    struct Minion* minion = getMinionFromFile(name);
    if (minion == NULL) {
        puts(" [ERROR] Failed to login minion!");
        return;
    }

    if (strcmp(password, minion->password) != 0) {
        puts(" [ERROR] Wrong minion password!");
        free(minion);
        return;
    }
    
    loggedInMinion = minion;
    puts(" [MINIONS] Logged in your minion!");
}

void showMyMinion() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] Minion is not logged in!");
        return;
    }
    char* family = loggedInMinion->family;
    if (strlen(family) == 0) {
        family = "None";
    }
    puts(MINION);
    printf("\t=> Name: %s\n\t=> Secret: %s\n\t=> Family: %s\n", loggedInMinion->name, loggedInMinion->secret, family);
}

void createFamily() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] Minion is not logged in!");
        return;
    }

    if (strlen(loggedInMinion->family)) {
        puts(" [ERROR] Your minion already has a family!");
        return;
    }

    char name[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter family name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    name[strcspn(name, "\n")] = 0;

    if (!strlen(name)) {
        puts(" [ERROR] Invalid family's name!");
        return;
    }

    if (checkFamilyExists(name)) {
        puts(" [ERROR] Family already exists!");
        return;
    }
    
    if (strstr(name, "..") != NULL || strstr(name, "/") != NULL) {
        puts(" [ERROR] Invalid family's name!");
        return;
    }

    char password[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter family password: ");
    if (fgets(password, sizeof(password), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    password[strcspn(password, "\n")] = 0;

    if (!strlen(password)) {
        puts(" [ERROR] Invalid family's password!");
        return;
    }

    struct Family* family = calloc(1, sizeof(struct Family));
    if (family == NULL) {
        puts(" [ERROR] Failed to create family!");
        return;
    }
    strcpy(family->name, name);
    strcpy(family->password, password);
    strcpy(family->minions[0], loggedInMinion->name);
    saveFamily(family);

    strcpy(loggedInMinion->family, family->name);
    saveMinion(loggedInMinion);

    free(family);
    puts(" [MINIONS] Family successfully created!");
}

void joinFamily() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] Minion is not logged in!");
        return;
    }

    if (strlen(loggedInMinion->family)) {
        puts(" [ERROR] Your minion already has a family!");
        return;
    }

    char name[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter family name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }
    name[strcspn(name, "\n")] = 0;

    if (!strlen(name)) {
        puts(" [ERROR] Invalid family's name!");
        return;
    }

    if (!checkFamilyExists(name)) {
        puts(" [ERROR] Family doesn't exist!");
        return;
    }

    struct Family* family = getFamilyFromFile(name);
    if (family == NULL) {
        puts(" [ERROR] Failed to get family!");
        return;
    }

    int family_size = getFamilySize(family);
    if (family_size == MAX_FAMILY_SIZE) {
        puts(" [ERROR] This family is already full!");
        free(family);
        return;
    }

    char password[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter family password: ");
    if (fgets(password, sizeof(password), stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        free(family);
        return;
    }
    password[strcspn(password, "\n")] = 0;
    if (!strlen(password)) {
        puts(" [ERROR] Invalid family's password!");
        free(family);
        return;
    }

    if (strcmp(password, family->password) != 0) {
        puts(" [ERROR] Wrong family's password!");
        free(family);
        return;
    }

    strcpy(family->minions[family_size], loggedInMinion->name);
    strcpy(loggedInMinion->family, family->name);

    saveFamily(family);
    free(family);

    saveMinion(loggedInMinion);
    puts(" [MINIONS] Successfully joined to the family!");
}

void familyInfo() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] Minion is not logged in!");
        return;
    }

    if (!strlen(loggedInMinion->family)) {
        puts(" [ERROR] Your minion doesn't have a family!");
        return;
    }

    struct Family* family = getFamilyFromFile(loggedInMinion->family);
    if (family == NULL) {
        puts(" [ERROR] Failed to get family!");
        return;
    }

    printf("\n [MINIONS] Here is your family <%s>:\n", family->name);

    printFamily(family);
    free(family);
}

void familyMinionInfo() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] Minion is not logged in!");
        return;
    }

    if (!strlen(loggedInMinion->family)) {
        puts(" [ERROR] Your minion doesn't have a family!");
        return;
    }

    char name[SMALL_DEFAULT_STRLEN];
    printf("\n [MINIONS] Enter minion's name to get info: ");
    if (fgets(name, BIG_DEFAULT_STRLEN, stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }

    name[strcspn(name, "\n")] = 0;
    if (!strlen(name)) {
        puts(" [ERROR] Invalid minion's name!");
        return;
    }

    struct Family* family = getFamilyFromFile(loggedInMinion->family);
    if (family == NULL) {
        puts(" [ERROR] Failed to get family!");
        return;
    }

    if (!isMinionExistsInFamily(family, name)) {
        puts(" [ERROR] Minion doesn't exist in your family!");
        free(family);
        return;
    }

    struct Minion* minion = getMinionFromFile(name);
    if (minion == NULL) {
        printf("\n [ERROR] Failed to get families's minion <%s>!", name);
        free(family);
        return;
    }
    printf("\n [MINIONS] Minion in your family <%s>:\n", family->name);
    printMinion(minion);
    printf("\n");
    free(minion);
    free(family);
}

void gruDoor() {
    puts(GRU);

    char password[SMALL_DEFAULT_STRLEN];
    printf("\n [GRUDOOR] Enter Gru password: ");
    if (fgets(password, SMALL_DEFAULT_STRLEN, stdin) == NULL) {
        puts(" [ERROR] Bad Input!");
        return;
    }

    password[strcspn(password, "\n")] = 0;
    if (!strlen(password)) {
        puts(" [ERROR] Invalid password!");
        return;
    }

    if (strcmp(password, GRUDOOR_PASSWORD) != 0) {
        puts(" [ERROR] Wrong password, little minion hahaha!");
        return;
    }
    
    gruAdmin();
}

void logout() {
    if (loggedInMinion == NULL) {
        puts(" [ERROR] You are not logged in!");
        return;
    }
    free(loggedInMinion);
    loggedInMinion = NULL;
    puts(" [MINIONS] Logged out!");
} 
