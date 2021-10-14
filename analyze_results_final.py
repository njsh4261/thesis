import csv
from scipy.stats.stats import trim_mean

HEADER = ["event", "trimmed mean"]

INDEX_EVENT = 1
INDEX_RATIO = 5

def analyze(input, output):
    with open(input, "r") as f1, open(output, "w", newline='') as f2:
        lines = [l for l in csv.reader(f1)]
        writer = csv.writer(f2)
        writer.writerow(HEADER)

        d = {}
        for line in lines[1:]:
            event, ratio = line[INDEX_EVENT], line[INDEX_RATIO]
            if event in d:
                d[event].append(float(ratio))
            else:
                d[event] = [float(ratio)]
        
        # print(d)
        for key in d.keys():
            writer.writerow([
                key, str(trim_mean(d[key], 0.1))
            ])

if __name__ == "__main__":
    analyze(
        "../core_pinned/perf_compare.csv",
        "../core_pinned/perf_trimmed_mean.csv"
    )