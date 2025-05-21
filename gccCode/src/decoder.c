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

    // Find the start of the hex data
    const char *hex_start = strstr(argv[1], "13xcf64=");
    if (!hex_start) {
        fprintf(stderr, "Error: Couldn't find hex data marker\n");
        return 1;
    }
    hex_start += 8; // Skip past "13xcf64="

    // Extract exactly 208 hex characters
    char clean_hex[209] = {0}; // 208 chars + null terminator
    int hex_chars = 0;
    
    while (*hex_start && hex_chars < 208) {
        if (isxdigit(*hex_start)) {
            clean_hex[hex_chars++] = *hex_start;
        }
        hex_start++;
    }

    if (hex_chars != 208) {
        fprintf(stderr, "Error: Expected 208 hex chars, got %d\n", hex_chars);
        fprintf(stderr, "Hex data: %s\n", clean_hex);
        return 1;
    }

    printf("Decoded complex numbers:\n");
    for (int i = 0; i < 13; i++) {
        // Get 8 bytes for real and imag parts
        char real_hex[9] = {0};
        char imag_hex[9] = {0};
        memcpy(real_hex, clean_hex + i*16, 8);
        memcpy(imag_hex, clean_hex + i*16 + 8, 8);

        // Convert to floats
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
