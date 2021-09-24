import numpy as np
from timeit import default_timer as timer
from numba import vectorize

@vectorize(["float32(float32, float32)"], target='cuda')
def vectorAdd(a, b):
    return a + b

def main():
    N = 32000000

    A = np.ones(N, dtype=np.float32)
    B = np.ones(N, dtype=np.float32)
    C = np.zeros(N, dtype=np.float32)

    star = timer()
    C = vectorAdd(A, B)
    vectoradd_time = timer() - start

    print(str(C[:5]))

    print(vectoradd_time)

if __name__ == '__main__':
    main()
