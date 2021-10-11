#ifndef _META_CPP_
#define _META_CPP_

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "data.h"
#include "math.h"

/*****************************************************************/
/*********************USER DECLARATION***********************/
/*****************************************************************/

//********
const int infinite = 2147483647;//max int

double  cost_sol;
double  best_cost_sol;

int max_global_iteration;

int* individual;           /* current solution (permutation) */
int* child;           /* current solution (permutation) */
int* Ex_individual;         	  /* solution to exchange */
int* Ex_individual_dual;
int* individual_dual;

int** population;
double* fitness_population;
int size_population;

int fitness;                      /* current cost                   */
int* best_individual;      /* best solution                  */
double best_fitness;              /* best cost                      */

int* full_X;

double current_parent_cost, Ex_parent_cost, tmp_cost, tmp_EXcost, child_cost;

clock_t iter_end,start,end;

/*****************************End User Declaration**********************/

/*****************************************************************/
/***********************USER FONCTION*************************/
/*****************************************************************/

/*************** L'Ecuyer random number generator ***************/
double rando(){
	  static int x10 = 12345, x11 = 67890, x12 = 13579, /* initial value*/
			  x20 = 24680, x21 = 98765, x22 = 43210; /* of seeds*/
	  const int m = 2147483647; const int m2 = 2145483479;
	  const int a12= 63308; const int q12=33921; const int r12=12979;
	  const int a13=-183326; const int q13=11714; const int r13=2883;
	  const int a21= 86098; const int q21=24919; const int r21= 7417;
	  const int a23=-539608; const int q23= 3976; const int r23=2071;
	  const double invm = 4.656612873077393e-10;
	  int h, p12, p13, p21, p23;
	  h = x10/q13; p13 = -a13*(x10-h*q13)-h*r13;
	  h = x11/q12; p12 = a12*(x11-h*q12)-h*r12;
	  if (p13 < 0) p13 = p13 + m; if (p12 < 0) p12 = p12 + m;
	  x10 = x11; x11 = x12; x12 = p12-p13; if (x12 < 0) x12 = x12 + m;
	  h = x20/q23; p23 = -a23*(x20-h*q23)-h*r23;
	  h = x22/q21; p21 = a21*(x22-h*q21)-h*r21;
	  if (p23 < 0) p23 = p23 + m2; if (p21 < 0) p21 = p21 + m2;
	  x20 = x21; x21 = x22; x22 = p21-p23; if(x22 < 0) x22 = x22 + m2;
	  if (x12 < x22) h = x12 - x22 + m; else h = x12 - x22;
	  if (h == 0) return(1.0); else return(h*invm);
 }

/*********** return an integer between low and high *************/
int unif(int low, int high){
	return low + (int)((double)(high - low + 1) * rando()) ;
}

void transpose(int *a, int *b) {int temp = *a; *a = *b; *b = temp;}

int minim(int a, int b) {if (a < b) return(a); else return(b);}

double cube(double x) {return x*x*x;}


void generate_random_solution(int n, int*  p){
	int i;
	for (i = 0; i < n;   i++) p[i] = i;
	for (i = 0; i < n-1; i++) transpose(&p[i], &p[unif(i, n-1)]);
}

void generate_tab_binaire(int Decimal, int*  full_X, int octet){

	int j;
	for(j=0;j<octet;j++) full_X[j] = -1;

	int i = 0;
	int correcteur = 0;

	int Binaire = 2;
	while (Binaire <= Decimal) Binaire *= 2;
	Binaire /= 2;
	while (Binaire != 0){
		if (Binaire <= Decimal){
			full_X[i] = 1; i++;
			Decimal -= Binaire;
		}
		else {full_X[i] = 0; i++;}
		Binaire /= 2;
	}

	for(i=0;i<octet;i++){
		if(full_X[i] == 0 || full_X[i] == 1) correcteur++;
	}
	if(correcteur != octet){
		j = octet;
		for(i=correcteur-1;i>=0;i--){
			full_X[j-1] = full_X[i];
			full_X[i] = 0;
			j--;
		}
	}
	for(i=0;i<octet;i++){
		if(full_X[i] == -1) full_X[i] = 0;
	}
}

/*-----------------------------------------------------------------------------------*/
/*       compute the cost difference if elements i and j    */
/*         are transposed in permutation (solution) p        */
/*-----------------------------------------------------------------------------------*/
double compute_delta(int n, int* a, int* b, int* p, int i, int j){
	int d; int k;
	d = (a[i*n+i]-a[j*n+j])*(b[p[j]*n+p[j]]-b[p[i]*n+p[i]]) +
	(a[i*n+j]-a[j*n+i])*(b[p[j]*n+p[i]]-b[p[i]*n+p[j]]);

	for (k = 0; k < n; k = k + 1){
		if (k!=i && k!=j){
			d = d + (a[k*n+i]-a[k*n+j])*(b[p[k]*n+p[j]]-b[p[k]*n+p[i]])
			+ (a[i*n+k]-a[j*n+k])*(b[p[j]*n+p[k]]-b[p[i]*n+p[k]]);
		}
	}
	return(d);
 }

/*---------------------------------------------------------------------------------------------*/
/*      Idem, but the value of delta[i][j] is supposed to              */
/*    be known before the transposition of elements r and s     */
/*---------------------------------------------------------------------------------------------*/
double compute_delta_part(int* a, int* b, int* p, int* delta,
					int i, int j, int r, int s,int n){
	return ( delta[i*n+j]+(a[r*n+i]-a[r*n+j]+a[s*n+j]-a[s*n+i]) *
	(b[p[s]*n+p[i]]-b[p[s]*n+p[j]]+b[p[r]*n+p[j]]-b[p[r]*n+p[i]]) +
	(a[i*n+r]-a[j*n+r]+a[j*n+s]-a[i*n+s]) *
	(b[p[i]*n+p[s]]-b[p[j]*n+p[s]]+b[p[j]*n+p[r]]-b[p[i]*n+p[r]])
	);
}

/*-----------------------------------------------------------------------------------*/
/*       compute the global fitness of the individuals    			     */
/*-----------------------------------------------------------------------------------*/
double compute_global_fitness(int* a, int* b, int* individual, int n){

	int i,j;
	double parent_cost = 0;

	for (i = 0; i < n; i = i + 1) for (j = 0; j < n; j = j + 1){
		parent_cost = parent_cost + a[i*n+j] * b[individual[i]*n+individual[j]];
	}

	return parent_cost;
}

// local search
// Perform improvements as soon as they are found
void local_search(int n, int*  a, int*  b, int*  p, double *cost){

	int r, s, i, j, nr_moves;
	double delta;

	// set of moves, numbered from 0 to index
	int* move;
	move = (int*) malloc((n*(n-1)/2)*sizeof(int));
	nr_moves = 0;

	for (i = 0; i < n-1; i++)
		for (j=i+1; j < n; j++) move[nr_moves++] = n*i+j;

	int improved = true;

	while(improved){

		improved = false;
		for (i = 0; i < nr_moves-1; i++) transpose(&move[i], &move[unif(i+1, nr_moves-1)]);
		for (i = 0; i < nr_moves; i++){

			r = move[i]/n;
			s = move[i]%n;
			delta = compute_delta(n, a, b, p, r, s);

			if (delta < 0){
				*cost += delta;
				transpose(&p[r], &p[s]);
				improved = true;
			}
		}
	}

	free(move);
}

void Uniform_crossover(int n, int* individual, int* Ex_individual, int* a, int* b)
{
	int* UX_Select;
	/*for the Standard UX crossover*/
	UX_Select = (int*)calloc(n, sizeof(int));
	for (int s = 0; s < n/2; s++) UX_Select[s] = 0;
	for (int s = n/2; s < n; s++) UX_Select[s] = 1;
	for (int i = 0; i < n-1; i++) transpose(&UX_Select[i], &UX_Select[unif(i, n-1)]);

	int* vide;
	int i, k;
	vide = (int*)calloc(n, sizeof(int));

	for (i = 0; i < n; i++) vide[i] = 0;

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 0){
			individual[i] = individual[i];
			vide[individual[i]] = 1;
		}
		else individual[i] = -1;
	}

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 1 && vide[Ex_individual[i]] == 0){
			individual[i] = Ex_individual[i];
			vide[individual[i]] = 1;
		}
	}

	k=0;
	int stop;
	for (i = 0; i < n; i++) {
		if(individual[i] == -1) {
			stop = 0;
			while(!stop){
				if(vide[k] == 0){
					individual[i] = k;
					vide[k] = 1;
					stop = 1;
				}
				else k++;
			}
		}
	}

	free(UX_Select);
	free(vide);
}

void One_point_crossover(int n, int* individual, int* Ex_individual, int* a, int* b)
{
	int* UX_Select;

	/*for the Standard UX crossover*/
	UX_Select = (int*)calloc(n, sizeof(int));
	for (int s = 0; s < n/2; s++) UX_Select[s] = 0;
	for (int s = n/2; s < n; s++) UX_Select[s] = 1;
	for (int i = 0; i < n-1; i++) transpose(&UX_Select[i], &UX_Select[unif(i, n-1)]);

	int* vide;
	int i, k;
	vide = (int*)calloc(n, sizeof(int));

	int point = rando() * n-1;

	for (int s = 0; s < point; s++) UX_Select[s] = 0;
	for (int s = point; s < n; s++) UX_Select[s] = 1;

	for (i = 0; i < n; i++) vide[i] = 0;

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 0){
			individual[i] = individual[i];
			vide[individual[i]] = 1;
		}
		else individual[i] = -1;
	}

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 1 && vide[Ex_individual[i]] == 0){
			individual[i] = Ex_individual[i];
			vide[individual[i]] = 1;
		}
	}

	k=0;
	int stop;
	for (i = 0; i < n; i++) {
		if(individual[i] == -1) {
			stop = 0;
			while(!stop){
				if(vide[k] == 0){
					individual[i] = k;
					vide[k] = 1;
					stop = 1;
				}
				else k++;
			}
		}
	}

	free(UX_Select);
	free(vide);
}

void Two_point_crossover(int n, int* individual, int* Ex_individual, int* a, int* b)
{
	int* UX_Select;

	/*for the Standard UX crossover*/
	UX_Select = (int*)calloc(n, sizeof(int));
	for (int s = 0; s < n/2; s++) UX_Select[s] = 0;
	for (int s = n/2; s < n; s++) UX_Select[s] = 1;
	for (int i = 0; i < n-1; i++) transpose(&UX_Select[i], &UX_Select[unif(i, n-1)]);

	int* vide;
	int i, k;
	vide = (int*)calloc(n, sizeof(int));

	int point1 = rando() * n-1;
	int point2 = ( rando() * ((n-1)-point1) ) + point1;

	for (int s = 0; s < point1; s++) UX_Select[s] = 0;
	for (int s = point1; s < point2; s++) UX_Select[s] = 1;
	for (int s = point2; s < n; s++) UX_Select[s] = 0;

	for (i = 0; i < n; i++) vide[i] = 0;

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 0){
			individual[i] = individual[i];
			vide[individual[i]] = 1;
		}
		else individual[i] = -1;
	}

  for (i = 0; i < n; i++) {
		if(UX_Select[i] == 1 && vide[Ex_individual[i]] == 0){
			individual[i] = Ex_individual[i];
			vide[individual[i]] = 1;
		}
	}


	k=0;
	int stop;
	for (i = 0; i < n; i++) {
		if(individual[i] == -1) {
			stop = 0;
			while(!stop){
				if(vide[k] == 0){
					individual[i] = k;
					vide[k] = 1;
					stop = 1;
				}
				else k++;
			}
		}
	}

	free(UX_Select);
	free(vide);
}

/***************************************End User Fonction******************************************/

void Meta_Init(int n, int* a, int* b, int Generations, int size_pop){
	/*
	This function perform the allocation and initialization of the structures needed for our generator
	*/

	max_global_iteration = Generations;
	size_population = size_pop;

	cost_sol  = 0.0;
	current_parent_cost = infinite;
	best_fitness = infinite;

	individual = (int*)calloc(n, sizeof(int));
	child = (int*)calloc(n, sizeof(int));
	Ex_individual = (int*)calloc(n, sizeof(int));

	best_individual = (int*)calloc(n, sizeof(int));

	population = (int**)calloc(size_population, sizeof(int*));
	for (int i = 0; i < size_population; i++) population[i] = (int*)calloc(n, sizeof(int));

	fitness_population = (double*)calloc(size_population, sizeof(double));

}

void Meta_Optimize(int n,int BKS,int* a,int* b, int Crossover, int memetic){
	/*
	This function perform the genetic hybrid algorithm to solve QAP
	*/

	start = clock();
	int global_iter = 0;
	int i;
	int old = 0;

	/***************Random Initialization**********************/
	for(i=0; i<size_population; i++){

			generate_random_solution(n, population[i]);
			fitness_population[i] = compute_global_fitness(a, b, population[i], n);

			if(fitness_population[i] < best_fitness){
				best_fitness = fitness_population[i];
				for (int k = 0; k < n; k = k+1) best_individual[k] = population[i][k];
			}
	}

	//Generations
	for(global_iter = 0; global_iter < max_global_iteration; global_iter++){

		//random select from the population
		int select1 = rando() * size_population;
		int select2 = rando() * size_population;

		//parent 1
		for (i = 0; i < n; i++) individual[i] = population[select1][i];
		current_parent_cost = fitness_population[select1];

		//parent 2
		for (i = 0; i < n; i++) {Ex_individual[i] = population[select2][i];}
		Ex_parent_cost = fitness_population[select2];

		switch(Crossover)
		{
			case 0 :
			   Uniform_crossover(n, individual, Ex_individual, a, b);
			   break;
			case 1 :
			   One_point_crossover(n, individual, Ex_individual, a, b);
			   break;
			case 2 :
			   Two_point_crossover(n, individual, Ex_individual, a, b);
			   break;
			default :
			   break;
		}

		//child
		for (int k = 0; k < n; k = k+1) child[k] = individual[k];
		child_cost = compute_global_fitness(a, b, child, n);

		if(memetic == 1)
		{
			 local_search(n, a, b, child, &child_cost);
		}

		iter_end = clock();

		if(child_cost < best_fitness){
			best_fitness = child_cost;
			for (int k = 0; k < n; k = k+1) best_individual[k] = child[k];
		}

		//Strategy : replace the oldest if ther is no fitness clone in the poupulation
		int clone = 0;
		//search firness clone
		for (i = 0; i < size_population; i++){
			if(child_cost == fitness_population[i]) clone = 1;
		}
		//remplacement
		if(!clone){

			for (i = 0; i < n; i++) population[old][i] = child[i];
			fitness_population[old] = child_cost;

			if(old == size_population - 1) old = 0;
			else old++;
		}

	}

	end = clock();

	cost_sol = best_fitness;

}

// Display and write results
void Meta_Display_results(FILE* fres, int n, int BKS, int run, int Generations, int size_pop, char* instance, int Crossover, int memetic, int c){
		/*
		This function write each row of our dataset
		*/

	   double Time = (double)(end-start)/CLOCKS_PER_SEC;
	   int j;

		 fprintf(fres,"%s\t",instance); //name of the instance
		 fprintf(fres,"%d\t",n);

		 if(c < 3) fprintf(fres,"T1\t");
		 else if(c<6) fprintf(fres,"T2\t");
		 else if(c<9) fprintf(fres,"T3\t");
		 else fprintf(fres,"T4\t");

		 switch(Crossover)
		 		{
					case 0 :
						fprintf(fres,"UX\t");
			 			 break;
			 		case 1 :
						fprintf(fres,"OPX\t");
			 			break;
			 		case 2 :
						fprintf(fres,"TPX\t");
			 			break;
			 		default :
			 			 break;
		 }

		 if(memetic == 0) fprintf(fres,"NO\t");
		 else fprintf(fres,"YES\t");

		 fprintf(fres,"%d\t%d\t%d\t",run, Generations, size_pop);

	   printf(" Solution: %f (trial %d) \n",  100*(cost_sol - BKS)/BKS, run);
	   for (j = 0; j < n; j++) printf("%d ", (best_individual[j]+1));// +1 pour l'affichage
	   printf("\n");
	   printf(" Execution time = [%.3lf] second (trial %d) \n", (double)(end-start)/CLOCKS_PER_SEC, run);

	   fprintf(fres,"%.3lf\t",Time);
	   fprintf(fres,"%f\n", 100*( cost_sol  - BKS)/BKS );

}


// Frees resources
void Meta_Free(){
	free(individual);
	free(child);
	free(Ex_individual);
	free(best_individual);
	free(population);
	free(fitness_population);
}

#endif
