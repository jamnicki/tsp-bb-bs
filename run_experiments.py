from pprint import pprint

import numpy as np

from generator import RandomNumberGenerator


def populate_distance_matrix(D, gen):
    n = D.shape[0]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            D[i, j] = gen.nextInt(1, 30)
    return D


def main():
    seed = 42
    gen = RandomNumberGenerator(seedVaule=seed)

    N = 10  # liczba punktów
    D = np.full(shape=(N, N), fill_value=np.nan)  # macierz odległości
    D = populate_distance_matrix(D, gen)

    pprint(D)


if __name__ == "__main__":
    main()
