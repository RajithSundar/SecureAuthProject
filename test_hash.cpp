#include <cstdint>
#include <cstdio>
#include <cstring>


// DJB2 Hash Function
uint32_t djb2_hash(const char *str) {
  uint32_t hash = 5381;
  int c;
  while ((c = *str++))
    hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
  return hash;
}

int main() {
  const char *password = "admin123";
  uint32_t hash = djb2_hash(password);
  printf("DJB2 hash of '%s' = %u\n", password, hash);
  return 0;
}
