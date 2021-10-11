#include "data.h"
void alloc_data(DATA *d){
	  d->a = new int[d->n*d->n];
	  d->b = new int[d->n*d->n];
   }
DATA *load_data(char *filename)
   {
      int i;
      DATA *d;
      FILE *fp;
      fp = fopen(filename, "r");
      if(fp == NULL)
	  {
		  fprintf(stderr, "Erreur ouverture fichier instances\n");
		  exit(0);
	  }
      d = new DATA;

      fscanf(fp,"%d%d\n", &d->n, &d->opt);

      alloc_data(d);

      /************** read flows and distances matrices **************/
      for(i=0; i<(d->n*d->n); i++)
			  {
				fscanf(fp, "%d",&(d->a[i]));
			  }
      for(i=0; i<(d->n*d->n); i++)
			  {
				fscanf(fp, "%d",&(d->b[i]));
			  }
      fclose(fp);
      return d;
   }
void print_data(DATA *d){
	int i,j;
	printf("Number of location and facilities: %d \n",d->n);
	for(i=0;i<d->n;i++){
		for(j=0;j<d->n;j++){
		printf("%d\t",d->a[(i*d->n)+j]);
		}
		printf("\n");
	}
        printf("********************\n");
	for(i=0;i<d->n;i++){
		for(j=0;j<d->n;j++){
		printf("%d\t",d->b[(i*d->n)+j]);
		}
		printf("\n");
	}
}

void free_data(DATA *d){
	delete[] (d->a);
	delete[] (d->b);
}
