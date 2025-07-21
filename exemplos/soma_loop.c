int main() {
  int i = 0;
  int soma = 0;

  while (i < 5) {
    soma = soma + i;
    i = i + 1;
  }

  printf(soma); // Esperado: 10 (0+1+2+3+4)
}
