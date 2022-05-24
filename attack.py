from util import *
import numpy as np
import time
from functools import partial
import concurrent.futures
import subprocess
import tqdm
import csv
import os


def cpa(traces, power_models):
    # Calculate the correlation matrix for each added trace.
    # Based on Version 6 in Computational aspects of correlation power analysis
    # but with even more precomputation to compute for all added traces.

    hyp = np.empty((len(power_models), len(traces), 256))

    for m, model in enumerate(power_models):
        hyp[m] = np.fromfunction(np.vectorize(model), (len(traces), 256), dtype=int)

    s1 = np.cumsum(traces, axis=0)[:, np.newaxis, :]
    s2 = np.cumsum(np.square(traces), axis=0)[:, np.newaxis, :]
    s3 = np.cumsum(hyp, axis=1)[:, :, :, np.newaxis]
    s4 = np.cumsum(np.square(hyp), axis=1)[:, :, :, np.newaxis]
    s5 = np.cumsum(traces[:, np.newaxis, :] * hyp[:, :, :, np.newaxis], axis=1)
    n = np.arange(1, len(traces) + 1)[:, np.newaxis, np.newaxis]
    # We ignore divide by zero warning, those calulations become NaN.
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.abs(
            (n * s5 - s1 * s3)
            / np.sqrt((n * s2 - np.square(s1)) * (n * s4 - np.square(s3)))
        )


def scores(corr):
    """Compute the scores for each key from a matrix of all correlations"""
    return np.max(corr, axis=len(corr.shape) - 1)


def keyrank(g, key):
    """Compute the rank of the correct key from a list of scores"""
    return np.where((-g).argsort() == key)[0][0]


def experiment(numtraces, key, byte, model, experiment):
    corr = scores(
        cpa(
            traces[numtraces * experiment : numtraces * (experiment + 1)],
            [
                model(
                    plaintexts[numtraces * experiment : numtraces * (experiment + 1)],
                    byte,
                    b,
                )
                for b in range(8)
            ],
        )
    )
    summ = np.sum(corr, axis=0)
    prodd = np.prod(corr, axis=0)
    maxx = np.max(corr, axis=0)

    results = {}
    for i in range(numtraces):
        for b in range(8):
            results[f"Bit {b}, {i}"] = keyrank(corr[b, i], key[byte])
        results[f"Sum, {i}"] = keyrank(summ[i], key[byte])
        results[f"Prod, {i}"] = keyrank(prodd[i], key[byte])
        results[f"Max, {i}"] = keyrank(maxx[i], key[byte])
    return results


def run_experiments(
    path,
    experiments,
    threads,
    num_traces,
    window_start,
    window_end,
    byte=0,
    model=two_bit_model,
    seed=None,
):
    key, plaintexts_original, _, traces_full = get_traces(path)
    assert traces_full.shape[0] >= num_traces * experiments

    seed_sequence = np.random.SeedSequence(seed)
    permutation = np.random.default_rng(seed_sequence).permutation(traces_full.shape[0])

    global traces
    traces = traces_full[permutation, window_start:window_end].copy()
    del traces_full

    global plaintexts
    plaintexts = plaintexts_original[permutation].copy()
    del plaintexts_original

    columns = []
    for i in range(num_traces):
        for b in range(8):
            columns.append(f"Bit {b}, {i}")
        columns.append(f"Sum, {i}")
        columns.append(f"Prod, {i}")
        columns.append(f"Max, {i}")

    with open(f"results/experiments-{int(time.time())}.csv", "w", newline="") as f:
        commit = (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("ascii")
            .strip()
        )
        f.write(
            f"Commit: {commit}, Trace file: {os.path.basename(path)}, Seed: {seed_sequence.entropy}, Experiments: {experiments}, Number of traces: {num_traces}, Window start: {window_start}, Window end: {window_end}, Byte: {str(byte)}, Power Model: {model.__name__}\n"
        )

        writer = csv.DictWriter(f, columns, delimiter=";")
        writer.writeheader()
        with concurrent.futures.ProcessPoolExecutor(threads) as executor:
            for results in tqdm.tqdm(
                executor.map(
                    partial(
                        experiment,
                        num_traces,
                        key,
                        byte,
                        model,
                    ),
                    range(experiments),
                ),
                total=experiments,
            ):
                writer.writerow(results)


def main():
    threads = 10

    run_experiments(
        "traces/2b7e151628aed2a6abf7158809cf4f3c-fix-500000-equal.csv",
        1000,
        threads,
        500,
        1100,
        1500,
    )

    run_experiments(
        "traces/2b7e151628aed2a6abf7158809cf4f3c-fix-500000-diff.csv",
        1000,
        threads,
        500,
        1100,
        1500,
    )


if __name__ == "__main__":
    main()
