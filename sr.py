from util import *
import os
import collections
import csv


def get_results(path):
    data = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(path) as f:
        f.readline()
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            for k, v in row.items():
                method, traces = [s.strip() for s in k.split(",")]
                data[method][int(traces)].append(int(v))
    return data


def transform_results(results, transform):
    data = collections.defaultdict(dict)

    for method, trace_dict in results.items():
        for traces, keyranks in trace_dict.items():
            data[traces][method] = transform([int(r) for r in keyranks])

    return data


def combine_results(results, labels):
    data = collections.defaultdict(dict)
    for d, l in zip(results, labels):
        for traces, method_dict in d.items():
            for k, v in method_dict.items():
                data[traces][l + " " + k] = v
    return data


def main():
    data = combine_results(
        [
            transform_results(
                get_results(path), lambda keyranks: keyranks.count(0) / len(keyranks)
            )
            for path in [
                "results/experiments-1650900926.csv",
                "results/experiments-1650903964.csv",
            ]
        ],
        ["Same", "Different"],
    )
    with open("data/success_rates.csv", "w") as f:
        fieldnames = ["Traces"] + list(data[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in data.items():
            v["Traces"] = k
        writer.writerow(v)


if __name__ == "__main__":
    main()
