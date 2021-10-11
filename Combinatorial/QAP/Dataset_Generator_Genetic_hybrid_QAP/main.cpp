/*-------------------------------------------------------------------------
  - Omar Abdelkafi
	This code contains fixes the quadratic assignment problem.
	It is a hybrid genetic algorithm with several possibilities of parallelization, crossover, hybridization and diversification.

	The objective is to generate a dataset in order to analyze the behavior of the different components

	to understand the crossover used here you can refer to :
	https://www.researchgate.net/publication/344080971_On_the_Design_of_a_Partition_Crossover_for_the_Quadratic_Assignment_Problem

	Compile the program on lunix : g++ -Wall -g main.cpp data.cpp Meta.cpp -o QAPDATASET
	Execution cmd : ./QAPDATASET
  ------------------------------------------------------------------------*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "data.h"
#include "Meta.h"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <cstdlib>


int main(int argc, char **argv){

	/*PARAMETERS*/
	FILE* global_file=NULL;
	char instance[30];

	int max_runs, run;
	int inst, c;
	int Crossover; //"0" UX, "1" OPX, "2" TPX
	int memetic; //"0" no memetic, "1" memetic with LS

	max_runs = 10;
	inst = 1;
	int Generations = 10000;
	int size_pop = 8;
	/*************/

	FILE * fres=fopen("Dataset_Genetic_hybrid_QAP.csv","w");
	fprintf(fres,"Instance\tsize\tType\tCrossover\thybridation\tNrun\tNGeneration\tsizepop\tTimes\tdeviation\n");
	global_file = fopen("FileGlobal.txt","r");

	for(c=0;c<inst;c++){

					fscanf(global_file,"%s\n", instance);

					/******** read file name and specifique data for the problem **********/

					int size;                      /* problem size        */
					int BKS;                       /* Best known solution */

					DATA *d;
					d = load_data(instance);
					print_data(d);

					size = d->n;
					BKS  = d->opt;

					/********************* Metaheuristic execution ************************/
					for(Crossover=0;Crossover<3;Crossover++){
						 for(memetic=0;memetic<2;memetic++){
													for(run = 0; run < max_runs; run++){

													Meta_Init(size, d->a, d->b, Generations, size_pop);

													Meta_Optimize(size, BKS, d->a, d->b, Crossover, memetic);

													Meta_Display_results(fres, size, BKS, run, Generations, size_pop, instance, Crossover, memetic, c);

													Meta_Free();

												}//End trials

						 }
					}

					free_data(d);
					fflush(stdin);

	}//fin global file

	fclose(global_file);
	fclose(fres);

	return EXIT_SUCCESS;
 }
