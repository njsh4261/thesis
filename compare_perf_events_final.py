import csv
from scipy.stats.stats import trim_mean

# INDEX_BENCH_NAME = 0
# INDEX_EVENT_NAME = 1
# INDEX_EVENT_RESULT = 2

INDEX_ITER = 0
INDEX_BENCH = 1
INDEX_EVENT = 2
INDEX_RESULT = 3

HEADER = [
    "bench_name", "event", "AMD_result", "Intel_result", "differences", "ratio"
]
RUNNING_TIME_HEADER = [
    "bench_name", "AMD_mean", "Intel_mean", "ratio",
]

NOT_SUPPORTED = "<not supported>"
INT_PATTERN = ""

def to_num(item):
    return float(item.replace(",", ""))

def csv_to_data(fd):
    result = {}
    event_set = set()
    bench_list = []
    running_times = {}

    for line in [l for l in csv.reader(fd)][1:]:
        if line[INDEX_RESULT] == "<not supported>" or line[INDEX_RESULT] == "<not counted>":
            continue

        if line[INDEX_EVENT].find("time-elapsed") != -1:
            if line[INDEX_BENCH] in running_times:
                running_times[line[INDEX_BENCH]].append(float(line[INDEX_RESULT]))
            else:
                running_times[line[INDEX_BENCH]] = [float(line[INDEX_RESULT])]
            continue

        event_set.add(line[INDEX_EVENT])
        if line[INDEX_BENCH] not in bench_list:
            bench_list.append(line[INDEX_BENCH])

        if line[INDEX_BENCH] in result:
            if line[INDEX_EVENT] not in line[INDEX_BENCH]:
                result[line[INDEX_BENCH]][line[INDEX_EVENT]] = [to_num(line[INDEX_RESULT])]
            else:
                result[line[INDEX_BENCH]][line[INDEX_EVENT]].append(to_num(line[INDEX_RESULT]))
        else:
            result[line[INDEX_BENCH]] = {line[INDEX_EVENT]: [to_num(line[INDEX_RESULT])]}
    
    result_avg = {}
    running_times_avg = {}
    for key1 in result.keys():
        for key2 in result[key1].keys():
            result_avg[(key1, key2)] = trim_mean(result[key1][key2], 0.1)
    for key in running_times.keys():
        running_times_avg[key] = trim_mean(running_times[key], 0.1)

    return result_avg, bench_list, event_set, running_times_avg

BENCH_ORDER = ["is", "ep", "cg", "mg", "ft", "bt", "sp", "lu", "ua", "dc"]
DATASET_ORDER = ["S", "W", "A", "B", "C", "D"]

def reorder_bench(bench_list):
    result = []
    for bo in BENCH_ORDER:
        for do in DATASET_ORDER:
            bench_name = bo + "." + do + ".x"
            if bench_name in bench_list:
                result.append(bench_name)
    return result

def compare_events(input1, input2, output1, output2):
    with open(input1, 'r') as f1, open(input2, 'r') as f2, \
         open(output1, 'w', newline='') as f3, open(output2, 'w', newline='') as f4:
        result1, bench_list, event_set1, running_times1 = csv_to_data(f1)
        result2, _,          event_set2, running_times2 = csv_to_data(f2)
        
        event_list_common = list(event_set1 & event_set2)
        event_list_common.sort()
        
        writer_comp = csv.writer(f3)
        writer_comp.writerow(HEADER)

        # print(event_list_common)
        # print(bench_list)
        # print(result1)

        # compare perf events
        for event in event_list_common:
            for bench in reorder_bench(bench_list):
                key = (bench, event)
                if (key in result1) and (key in result2):
                    new_row = [bench, event, result1[key], result2[key]]
                    if result1[key] != 0.0 and result2[key] != 0.0:
                        new_row += [result1[key] - result2[key], result1[key] / result2[key]]
                        writer_comp.writerow(new_row)
        
        # compare benchmark running time
        # print(running_times1)
        # print(running_times2)

        writer_runtime = csv.writer(f4)
        writer_runtime.writerow(RUNNING_TIME_HEADER)
        for bench in bench_list:
            writer_runtime.writerow([
                bench, running_times1[bench], running_times2[bench],
                running_times1[bench]/running_times2[bench]
            ])
            

if __name__ == '__main__':
    # compare_events(
    #     "../test_perf/amd_result_perf_cut3.csv",
    #     "../test_perf/intel_result_perf_cut3.csv",
    #     "../test_perf/perf_compare3.csv",
    #     "../test_perf/perf_compare_cut_not_supported3.csv",
    #     "../test_perf/perf_compare_running_time3.csv"
    # )

    compare_events(
        "../core_pinned/amd_result_perf_iter10.csv",
        "../core_pinned/intel_result_perf_iter10.csv",
        "../core_pinned/perf_compare.csv",
        "../core_pinned/perf_compare_running_times.csv"
    )

# " <not supported>"