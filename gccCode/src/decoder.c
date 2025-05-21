#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h> // For ntohl()

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <raw_iree_output>\n", argv[0]);
        return 1;
    }

    // Find hex data
    const char *hex_start = strstr(argv[1], "13xcf64=");
    if (!hex_start) {
        fprintf(stderr, "ERROR: Hex data marker not found\n");
        return 1;
    }
    hex_start += 8; // Skip past "13xcf64="

    // Extract exactly 208 hex chars (13 numbers * 16 chars)
    char hex[209] = {0};
    int count = 0;
    for (const char *p = hex_start; *p && count < 208; p++) {
        if ((*p >= '0' && *p <= '9') || (*p >= 'A' && *p <= 'F') || (*p >= 'a' && *p <= 'f')) {
            hex[count++] = *p;
        }
    }

    if (count != 208) {
        fprintf(stderr, "ERROR: Need 208 hex chars, found %d\n", count);
        return 1;
    }

    printf("Decoded complex numbers:\n");
    for (int i = 0; i < 13; i++) {
        // Extract 8 bytes for real and imag
        char real_hex[9] = {0};
        char imag_hex[9] = {0};
        strncpy(real_hex, hex + i*16, 8);
        strncpy(imag_hex, hex + i*16 + 8, 8);

        // Convert to network byte order (big-endian)
        uint32_t real_int = strtoul(real_hex, NULL, 16);
        uint32_t imag_int = strtoul(imag_hex, NULL, 16);
        real_int = ntohl(real_int);  // Fix endianness
        imag_int = ntohl(imag_int);  // Fix endianness

        // Interpret as IEEE 754 floats
        float real = *(float*)&real_int;
        float imag = *(float*)&imag_int;

        printf("[%02d] (r%.1f + i%.1fj)\n", i+1, real, imag);
    }
    return 0;
}
