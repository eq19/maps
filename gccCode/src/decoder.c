#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <raw_iree_output>\n", argv[0]);
        return 1;
    }

    // Find the hex data in the IREE output
    const char *p = strstr(argv[1], "13xcf64=");
    if (!p) {
        fprintf(stderr, "Error: Couldn't find hex data in input\n");
        return 1;
    }
    p += 8; // Skip past "13xcf64="

    // Extract and clean hex string
    char clean_hex[256] = {0};
    int j = 0;
    for (int i = 0; p[i] && j < 208; i++) {
        if (isxdigit(p[i])) {
            clean_hex[j++] = p[i];
        }
    }
    clean_hex[j] = '\0';

    if (strlen(clean_hex) != 208) {
        fprintf(stderr, "Error: Need exactly 208 hex chars (got %zu)\n", strlen(clean_hex));
        return 1;
    }

    printf("Decoded complex numbers:\n");
    for (int i = 0; i < 13; i++) {
        // Extract real and imag parts
        char real_hex[9] = {0};
        char imag_hex[9] = {0};
        strncpy(real_hex, clean_hex + i*16, 8);
        strncpy(imag_hex, clean_hex + i*16 + 8, 8);

        // Convert to floats
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
