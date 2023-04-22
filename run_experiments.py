from pprint import pprint
from time import perf_counter

import numpy as np
import pandas as pd
from tqdm import tqdm

import branch_and_bound
from generator import RandomNumberGenerator


def populate_distance_matrix(D, gen):
    n = D.shape[0]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            D[i, j] = gen.nextInt(1, 30)
    return D


def plot_execution_time():
    pass


def main():
    DEBUG = False

    seed_list = [1, 42, 666, 2137]
    N_list = [5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    bb_solutions = []
    bs_solutions = []
    for seed in tqdm(seed_list, desc=" Seed values: ", position=0):
        for N in tqdm(N_list, desc="Matrix sizes: ", position=1, leave=False):
            gen = RandomNumberGenerator(seedVaule=seed)

            D = np.full(shape=(N, N), fill_value=np.nan)  # macierz odległości
            D = populate_distance_matrix(D, gen)

            if DEBUG:
                print(" Distance matrix ".center(100, "*"), "\n")
                pprint(D)

            bb_pc0 = perf_counter()
            bb_path, bb_lenght = branch_and_bound.travel(D)
            bb_execution_time = perf_counter() - bb_pc0

            if DEBUG:
                print("\n", " Branch and Bound ".center(100, "*"), "\n")
                print(f"Path: {bb_path}")
                print(f"Length: {bb_lenght}")
                print(f"Execution time: {bb_execution_time:.6f}s")

            bb_solutions.append(
                {
                    "Algorithm": "Branch and Bound",
                    "MatrixSize": N,
                    "Seed": seed,
                    "Path": bb_path,
                    "Length": bb_lenght,
                    "Time": bb_execution_time,
                }
            )

            # print("\n", " Beam Search ".center(100, "*"), "\n")

            # exit()

    df = pd.DataFrame.from_dict(bb_solutions)
    df.to_csv("data/tsp_solution_results.csv", index=False)

    print("\n", "DONE!")


if __name__ == "__main__":
    main()
