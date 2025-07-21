int fat(int n) {
  if (n <= 1) {
    return 1;
  }
  return n * fat(n - 1);
}

int main() {
  int resultado = fat(5);
  printf(resultado); // Esperado: 120
}
