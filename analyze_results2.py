import csv

INDEX_EVENT = 0
INDEX_RATIO = 4

HEADER = ["event", "count", "ration_mean", ">1", ">1.3", "<1", "<0.7"]

RATIOS = 0
COUNT_MORE = 1
COUNT_MORE_30PERCENT = 2
COUNT_LESS = 3
COUNT_LESS_30PERCENT = 4

with open("../test_perf/perf_compare_cut_not_supported3.csv", "r") as f1, \
     open("../test_perf/perf_compare_summary3.csv", "w", newline="") as f2:
    lines = [l for l in csv.reader(f1)]
    result = {}
    events = []
    for line in lines[1:]:
        if line[INDEX_EVENT] not in result:
            result[line[INDEX_EVENT]] = {
                RATIOS: [],
                COUNT_MORE: 0,
                COUNT_MORE_30PERCENT: 0,
                COUNT_LESS: 0,
                COUNT_LESS_30PERCENT: 0,
            }
            events.append(line[INDEX_EVENT])
        else:
            ratio = float(line[INDEX_RATIO])
            result[line[INDEX_EVENT]][RATIOS].append(ratio)
            if ratio > 1.0:
                if ratio > 1.3:
                    result[line[INDEX_EVENT]][COUNT_MORE_30PERCENT] += 1
                result[line[INDEX_EVENT]][COUNT_MORE] += 1
            else:
                if ratio < 0.7:
                    result[line[INDEX_EVENT]][COUNT_LESS_30PERCENT] += 1
                result[line[INDEX_EVENT]][COUNT_LESS] += 1

    writer = csv.writer(f2)
    writer.writerow(HEADER)
    for event in events:
        writer.writerow([
            event,
            len(result[event][RATIOS]),
            sum(result[event][RATIOS])/len(result[event][RATIOS]),
            result[event][COUNT_MORE],
            result[event][COUNT_MORE_30PERCENT],
            result[event][COUNT_LESS],
            result[event][COUNT_LESS_30PERCENT],
        ])
