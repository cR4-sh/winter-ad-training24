#include <stdbool.h>

bool checkMinionExists(char* minionName);
bool checkFamilyExists(char* familyName);

void saveMinion(struct Minion* minion);
void saveFamily(struct Family* family);

struct Minion* getMinionFromFile(char* minionName);
struct Family* getFamilyFromFile(char* familyName);

int getFamilySize(struct Family* family);

void printMinion(struct Minion* minion);
void printFamily(struct Family* family);

bool isMinionExistsInFamily(struct Family* family, char *minionName);