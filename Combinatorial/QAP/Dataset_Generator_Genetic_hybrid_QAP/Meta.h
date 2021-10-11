#ifndef _META_H_
#define _META_H_

void Meta_Init(int size, int* a, int* b, int Generations, int size_pop);

void Meta_Optimize(int size,int opt,int* a,int* b, int Crossover, int memetic);

void Meta_Display_results(FILE* fres, int size, int BKS, int run, int Generations, int size_pop, char* instance, int Crossover, int memetic, int c);

void Meta_Free();

#endif
