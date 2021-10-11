#ifndef DATA_H_
#define DATA_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
struct DATA {
	int n;//size of the problem
	int opt;//BKS
	int *a;//flow matrix
	int *b;//distance matrix
};

   void alloc_data(DATA *d);

   DATA *load_data(char *filename);

   void print_data(DATA *d);

   void free_data(DATA *d);

   #endif
