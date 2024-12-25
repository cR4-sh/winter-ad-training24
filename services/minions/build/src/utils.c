#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#include <minions.h>
#include <utils.h>

bool checkMinionExists(char* minionName) {
    char filename[BIG_DEFAULT_STRLEN] = MINIONS_FOLDER;
    strcat(filename, minionName);

    if (access(filename, F_OK) == 0) {
       return true;
    } 
    return false;
}

bool checkFamilyExists(char* familyName) {
    char filename[BIG_DEFAULT_STRLEN] = FAMILIES_FOLDER;
    strcat(filename, familyName);

    if (access(filename, F_OK) == 0) {
       return true;
    } 
    return false;
}

void saveMinion(struct Minion* minion) {
    char filename[BIG_DEFAULT_STRLEN] = MINIONS_FOLDER;
    strcat(filename, minion->name);

    FILE *file = fopen(filename, "wb");
     if (file == NULL) {
        puts(" [ERROR] Failed to create minion!");
        return;
    }

    if (fwrite(minion, sizeof(struct Minion), 1, file) != 1) {
        puts(" [ERROR] Failed to create minion!");
    }
    fclose(file);
}

void saveFamily(struct Family* family) {
    char filename[BIG_DEFAULT_STRLEN] = FAMILIES_FOLDER;
    strcat(filename, family->name);

    FILE *file = fopen(filename, "wb");
     if (file == NULL) {
        puts(" [ERROR] Failed to save family!");
        return;
    }

    if (fwrite(family, sizeof(struct Family), 1, file) != 1) {
        puts(" [ERROR] Failed to save family!");
    }
    fclose(file);
}

struct Minion* getMinionFromFile(char* minionName) {
    char filename[BIG_DEFAULT_STRLEN] = MINIONS_FOLDER;
    strcat(filename, minionName);
    
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        return NULL;
    }

    struct Minion* minion = (struct Minion*)calloc(1, sizeof(struct Minion));
    if (fread(minion, sizeof(struct Minion), 1, file) != 1) {
        return NULL;
    }

    return minion;
}

struct Family* getFamilyFromFile(char* familyName) {
    char filename[BIG_DEFAULT_STRLEN] = FAMILIES_FOLDER;
    strcat(filename, familyName);
    
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        return NULL;
    }

    struct Family* family = (struct Family*)calloc(1, sizeof(struct Family));
    if (fread(family, sizeof(struct Minion), 1, file) != 1) {
        return NULL;
    }

    return family;
}

int getFamilySize(struct Family* family) {
    int length = 0;
    while (length < MAX_FAMILY_SIZE) {
        if (!strlen(family->minions[length])) {
            break;
        }
        length += 1;
    }
    return length;
}

void printMinion(struct Minion* minion) {
    printf("\n\t[%s]\n\t => Secret: %s", minion->name, minion->secret);
}

void printFamily(struct Family* family) {
    for (int i = 0; i < getFamilySize(family); ++i) {
        struct Minion* minion = getMinionFromFile(family->minions[i]);
        if (minion == NULL) {
            printf("\n [ERROR] Failed to get families's minion <%s>!", family->minions[i]);
            continue;
        }
        printMinion(minion);
        free(minion);
    }
    printf("\n");
}

bool isMinionExistsInFamily(struct Family* family, char *minionName) {
    for (int i = 0; i < getFamilySize(family); ++i) {
        if (strcmp(family->minions[i], minionName) == 0) {
            return true;
        } 
    }
    return false;
}