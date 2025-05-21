#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <full_hex_string>\n", argv[0]);
        return 1;
    }

    // Remove all whitespace from hex string
    char *hex = argv[1];
    char clean_hex[256] = {0};
    int j = 0;
    for (int i = 0; hex[i]; i++) {
        if (isxdigit(hex[i])) {
            clean_hex[j++] = hex[i];
        }
    }
    clean_hex[j] = '\0';

    if (strlen(clean_hex) < 13*16) {
        fprintf(stderr, "Error: Hex string too short (got %zu, need 208)\n", strlen(clean_hex));
        return 1;
    }

    printf("Decoded complex numbers:\n");
    for (int i = 0; i < 13; i++) {
        // Extract 8 bytes for real and imag parts
        char real_hex[9] = {0};
        char imag_hex[9] = {0};
        strncpy(real_hex, clean_hex + i*16, 8);
        strncpy(imag_hex, clean_hex + i*16 + 8, 8);

        // Convert to 32-bit integers
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);

        // Interpret as IEEE 754 floats
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
