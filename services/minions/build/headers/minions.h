#define SMALL_DEFAULT_STRLEN 64
#define BIG_DEFAULT_STRLEN 128

#define MINIONS_FOLDER "./minion_users/"
#define FAMILIES_FOLDER "./minion_families/"

#define MAX_FAMILY_SIZE 5
#define GRUDOOR_PASSWORD "GrU_1s_4llw4y$_w4tch1ng_U"

struct Minion {
    char name[SMALL_DEFAULT_STRLEN];
    char password[SMALL_DEFAULT_STRLEN];
    char secret[SMALL_DEFAULT_STRLEN];
    char family[SMALL_DEFAULT_STRLEN];
};

struct Family {
    char name[SMALL_DEFAULT_STRLEN];
    char password[SMALL_DEFAULT_STRLEN];
    char minions[MAX_FAMILY_SIZE][SMALL_DEFAULT_STRLEN];
};

void registerMinion();
void loginMinion();

void showMyMinion();
void createFamily();
void joinFamily();

void familyInfo();
void familyMinionInfo();

void gruDoor();

void logout();