import csv

INDEX_RESULT = 0
INDEX_EVENT_NAME = 1
INDEX_OTHERS = 2
INDEX_CLOCK_OTHERS = 1

def cut_redundant(input, output):
    with open(input, "r") as f1, open(output, "w", newline="") as f2:
        writer = csv.writer(f2)
        lines = [l for l in csv.reader(f1)]

        writer.writerow(lines[0])
        get_bench_name = True
        bench_name = ""
        for line in lines[1:]:
            if len(line) == 0:
                get_bench_name = True
            elif len(line) == 1:
                writer.writerow(line)
            elif get_bench_name:
                bench_name = "".join(line)
                get_bench_name = False
            else:
                if "#" in line:
                    del line[line.index("#")]
                if " #" in line:
                    del line[line.index(" #")]

                if line[0][-5:] == "clock":
                    split = line[INDEX_RESULT].split()
                    writer.writerow(
                        [
                            bench_name,
                            split[-1], split[0],
                            "msec"
                        ] + line[INDEX_CLOCK_OTHERS:]
                    )
                else:
                    writer.writerow(
                        [
                            bench_name, line[INDEX_EVENT_NAME], line[INDEX_RESULT]
                        ] + line[INDEX_OTHERS:]
                    )

if __name__ == "__main__":
    cut_redundant("../test_perf/middle3/amd_result_perf_trim3.csv", "../test_perf/amd_result_perf_cut3.csv")
    cut_redundant("../test_perf/middle3/intel_result_perf_trim3.csv", "../test_perf/intel_result_perf_cut3.csv")
