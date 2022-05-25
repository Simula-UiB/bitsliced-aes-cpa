from util import *
import collections
import numpy as np
import collections


def snr_plot(traces, model):
    data = collections.defaultdict(list)
    for i in range(len(traces)):
        data[model(i)].append(traces[i])
    means = {}
    for k, v in data.items():
        arr = np.array(v)
        means[k] = np.mean(arr, axis=0)
    signal = np.empty_like(traces)
    noise = np.empty_like(traces)
    for i in range(len(traces)):
        signal[i] = means[model(i)]
        noise[i] = traces[i] - means[model(i)]
    return np.var(signal, axis=0) / np.var(noise, axis=0)


def main():
    key, plaintexts, _, traces = get_traces(
        "traces/2b7e151628aed2a6abf7158809cf4f3c-fix-500000-diff.csv", 5000
    )

    snrs = []
    for b in range(8):
        snrs.append(
            snr_plot(traces, lambda i: two_bit_model(plaintexts, 0, b)(i, key[0]))
        )
    with open("data/snr_bits.csv", "w") as f:
        fieldnames = ["Time"] + [f"Bit {i}" for i in range(8)]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1100, 1450):
            row = {"Time": i}
            for b in range(8):
                row[f"Bit {b}"] = snrs[b][i]
            writer.writerow(row)


if __name__ == "__main__":
    main()
