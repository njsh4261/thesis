import csv

# with open("../test_perf/middle3/intel_result_perf3.csv", "r") as f1, open("../test_perf/middle3/intel_result_perf_trim3.csv", "w", newline='') as f2:
with open("../test_perf/middle3/amd_result_perf3.csv", "r") as f1, open("../test_perf/middle3/amd_result_perf_trim3.csv", "w", newline='') as f2:
    writer = csv.writer(f2)
    for line in csv.reader(f1):
        writer.writerow([item for item in line if len(item) > 0])