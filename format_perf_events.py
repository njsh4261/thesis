import csv, re

def format_perf_event(perf_file, input, output):
    with open(perf_file, "r") as f1, open(input, "r") as f2, open(output, "w", newline="") as f3:
        perf_list = [a.split()[0] for a in f1.readlines()]
        writer = csv.writer(f3)
        for l in csv.reader(f2):
            if l[1] != "perf (perf_events generic PMU)":
                writer.writerow(l)
            else:
                pattern = re.compile(l[0], re.IGNORECASE)
                new_event_code = ""
                for pl in perf_list:
                    if pattern.match(pl) is not None:
                        new_event_code = pl
                        break
                if new_event_code != "":
                    writer.writerow([new_event_code] + [l[1]] + [new_event_code] + l[3:])
                else:
                    writer.writerow(l)


if __name__ == "__main__":
    format_perf_event(
        "../test_omp_thrd16/plist_amd.txt",
        "../test_omp_thrd16/amd_codes_16.csv",
        "../test_omp_thrd16/amd_codes_16_2.csv"
    )
    format_perf_event(
        "../test_omp_thrd16/plist_intel.txt",
        "../test_omp_thrd16/intel_codes_16.csv",
        "../test_omp_thrd16/intel_codes_16_2.csv"
    )
