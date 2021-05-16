#include <stdio.h>
#define mod(a, b) (((a % b) + b) % b)
#define printh(a, b) printf("0x%2.2X%c", a, b)

unsigned char arrIP[] = {58, 50, 42, 34, 26, 18, 10, 2,
			 60, 52, 44, 36, 28, 20, 12, 4,
			 62, 54, 46, 38, 30, 22, 14, 6,
			 64, 56, 48, 40, 32, 24, 16, 8,
			 57, 49, 41, 33, 25, 17,  9, 1,
			 59, 51, 43, 35, 27, 19, 11, 3,
			 61, 53, 45, 37, 29, 21, 13, 5,
			 63, 55, 47, 39, 31, 23, 15, 7};

unsigned char arrIP_1[] = {40, 8, 48, 16, 56, 24, 64, 32,
                            39, 7, 47, 15, 55, 23, 63, 31,
                            38, 6, 46, 14, 54, 22, 62, 30,
                            37, 5, 45, 13, 53, 21, 61, 29,
                            36, 4, 44, 12, 52, 20, 60, 28,
                            35, 3, 43, 11, 51, 19, 59, 27,
                            34, 2, 42, 10, 50, 18, 58, 26,
                            33, 1, 41,  9, 49, 17, 57, 25};

void makePermutation(unsigned char *m, unsigned char *r, unsigned char *IP, unsigned char exp)
{
	unsigned char i, j = 0;
	unsigned char row, column, count = 0;
	for (i = 0; i < 64; i++)
	{
		if (count == 8) {j++; count = 0;}
		row = IP[i] >> 3;
		column = mod(IP[i], 8);
		if (j == exp) row--;
		if ((m[row] & (128 >> mod(column - 1, 8))))
			r[j] |= (128 >> count);
		count++;
	}
}

int main()
{
	unsigned char i;
	unsigned char r[8] = {0}, ir[8] = {0};

	makePermutation("Diamante", r, arrIP, 3);

	for (i = 0; i < 8; i++)
		printh(r[i], ' ');

	printf("\n");
	makePermutation(r, ir, arrIP_1, 0);

	for (i = 0; i < 8; i++)
		printf("%c", ir[i]);
	printf("\n");
	return 0;
}
