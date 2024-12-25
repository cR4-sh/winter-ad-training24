#include <stdio.h>
#include <stdint.h>

#include <banners.h>
#include <logic.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

    logic();
    return 0;
}

