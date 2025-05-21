#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <hex_string>\n", argv[0]);
        return 1;
    }

    char *hex = argv[1];
    for (int i = 0; i < 13; i++) {
        // Extract 8 bytes (1 complex number) at a time
        char real_hex[9];
        char imag_hex[9];
        snprintf(real_hex, 9, "%s", hex + i*16);
        snprintf(imag_hex, 9, "%s", hex + i*16 + 8);

        // Convert to floats
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
