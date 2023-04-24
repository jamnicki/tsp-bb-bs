from pprint import pprint
from time import perf_counter

import numpy as np
import pandas as pd
from tqdm import tqdm

import branch_and_bound
from generator import RandomNumberGenerator
import beam_search

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

    experiment_number = 5
    seed_list = [1, 42, 666, 2137, 321, 1435]
    N_list = [5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    bb_solutions = []
    bs_solutions = []
    for seed in tqdm(seed_list, desc=" Seed values: ", position=0):
        for N in tqdm(N_list, desc="Matrix sizes: ", position=1, leave=False):
            for i in range(experiment_number):
                gen = RandomNumberGenerator(seedVaule=seed)

                D = np.full(shape=(N, N), fill_value=np.nan)  # macierz odległości
                D = populate_distance_matrix(D, gen)

                if DEBUG:
                    print(" Distance matrix ".center(100, "*"), "\n")
                    pprint(D)

                bb_pc0 = perf_counter()
                bb_path, bb_lenght = branch_and_bound.travel(D)
                bb_execution_time = perf_counter() - bb_pc0

                bs_pc0 = perf_counter()
                bs_path, bs_lenght = beam_search.travel(D)
                bs_execution_time = perf_counter() - bs_pc0

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
                        "Experiment number": i,
                        "Time": bb_execution_time,
                    }
                )

                bs_solutions.append(
                    {
                        "Algorithm": "Beam Search",
                        "MatrixSize": N,
                        "Seed": seed,
                        "Path": bs_path,
                        "Length": bs_lenght,
                        "Experiment number": i,
                        "Time": bs_execution_time,
                    }
                )

                # print("\n", " Beam Search ".center(100, "*"), "\n")

                # exit()

    df = pd.DataFrame.from_dict(bb_solutions)
    df.to_csv("data/tsp_solution_results.csv", index=False)

    df = pd.DataFrame.from_dict(bs_solutions)
    df.to_csv("data/tsp_bs_results.csv", index=False)

    print("\n", "DONE!")


def beam_width_experiment():
    experiment_number = 5
    seed_list = [1, 42, 666, 2137, 3213, 2, 323]
    N_list = [30]
    beam_width_list = [1, 4, 7, 10, 13]

    bs_solutions = []
    for seed in tqdm(seed_list, desc=" Seed values: ", position=0):
        for N in tqdm(N_list, desc="Matrix sizes: ", position=1, leave=False):
            for beam_width in tqdm(beam_width_list, desc="Beam width values: ", position=2):
                for i in range(experiment_number):
                    gen = RandomNumberGenerator(seedVaule=seed)

                    D = np.full(shape=(N, N), fill_value=np.nan)  # macierz odległości
                    D = populate_distance_matrix(D, gen)

                    bs_pc0 = perf_counter()
                    bs_path, bs_lenght = beam_search.travel(D, beam_width=beam_width)
                    bs_execution_time = perf_counter() - bs_pc0

                    bs_solutions.append(
                        {
                            "Algorithm": "Beam Search",
                            "MatrixSize": N,
                            "Seed": seed,
                            "Path": bs_path,
                            "Length": bs_lenght,
                            "Experiment number": i,
                            "Beam width": beam_width,
                            "Time": bs_execution_time,
                        }
                    )

    df = pd.DataFrame.from_dict(bs_solutions)
    df.to_csv("data/tsp_bs_beam_width_matrix_30_results.csv", index=False)

    print("\n", "DONE!")


if __name__ == "__main__":
    # main()
    beam_width_experiment()
