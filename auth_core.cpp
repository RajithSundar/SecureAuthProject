#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>

// --- Security Constants ---
// DJB2 hash of "admin123"
const uint32_t STORED_PASSWORD_HASH =
    407908580UL; // Verified DJB2 hash for "admin123"
const char *TOTP_SECRET = "MY_SUPER_SECRET_KEY";

// --- Helper Functions ---

// DJB2 Hash Function
uint32_t djb2_hash(const char *str) {
  uint32_t hash = 5381;
  int c;
  while ((c = *str++))
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
  return hash;
}

// Secure String Copy to prevent buffer overflows
// Copies at most dest_size - 1 characters, ensuring null termination.
void secure_strcpy(char *dest, const char *src, size_t dest_size) {
  if (dest_size == 0)
    return;

  // Use strncpy for bounded copy
  strncpy(dest, src, dest_size - 1);

  // Explicitly ensure null termination
  dest[dest_size - 1] = '\0';
}

// Generate TOTP code based on time and secret
// Simplified TOTP: (Time / 30 + Hash(Secret)) % 1000000
int generate_totp(time_t current_time) {
  uint32_t secret_hash = djb2_hash(TOTP_SECRET);
  uint32_t time_step = (uint32_t)(current_time / 30);

  // Combine time and secret
  uint32_t combined = time_step + secret_hash;

  // Generate 6-digit code
  return combined % 1000000;
}

// --- Exported Functions for Python ---

extern "C" {

// Validate Login Credentials
// Returns true if username is "admin" and password hash matches.
bool validate_login(const char *username, const char *password) {
  // Securely copy inputs to local buffers to demonstrate secure_strcpy usage
  char safe_username[50];
  char safe_password[50];

  secure_strcpy(safe_username, username, sizeof(safe_username));
  secure_strcpy(safe_password, password, sizeof(safe_password));

  // Debug output to console (visible in the terminal running build.py)
  printf("[DEBUG] C++ Received Username: '%s'\n", safe_username);

  // Check username
  if (strcmp(safe_username, "admin") != 0) {
    printf("[DEBUG] Username mismatch.\n");
    return false;
  }

  // Check password hash
  uint32_t input_hash = djb2_hash(safe_password);
  printf("[DEBUG] Password Hash: %u, Expected: %u\n", input_hash,
         STORED_PASSWORD_HASH);

  return input_hash == STORED_PASSWORD_HASH;
}

// Get Current TOTP (For Demo/Debugging)
int get_current_totp() { return generate_totp(std::time(0)); }

// Validate User's TOTP Input
bool validate_totp(int user_code) {
  time_t now = std::time(0);

  // Check current window
  if (generate_totp(now) == user_code)
    return true;

  // Check previous window (to allow for slight time drift/delay)
  if (generate_totp(now - 30) == user_code)
    return true;

  return false;
}
}
