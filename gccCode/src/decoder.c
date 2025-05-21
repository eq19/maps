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

    // Find hex data by scanning for pattern
    const char *p = argv[1];
    while (*p) {
        if (strncmp(p, "13xcf64=", 8) == 0) {
            p += 8; // Skip marker
            break;
        }
        p++;
    }

    if (!*p) {
        fprintf(stderr, "ERROR: Hex data marker not found in:\n%s\n", argv[1]);
        return 1;
    }

    // Extract exactly 208 hex chars
    char hex[209] = {0};
    int count = 0;
    while (*p && count < 208) {
        if (isxdigit(*p)) {
            hex[count++] = *p;
        }
        p++;
    }

    if (count != 208) {
        fprintf(stderr, "ERROR: Need 208 hex chars, found %d\nHex data: %s\n", count, hex);
        return 1;
    }

    printf("Decoded complex numbers:\n");
    for (int i = 0; i < 13; i++) {
        // Extract each complex number
        char real_hex[9] = {0};
        char imag_hex[9] = {0};
        strncpy(real_hex, hex + i*16, 8);
        strncpy(imag_hex, hex + i*16 + 8, 8);

        // Convert to floats
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
