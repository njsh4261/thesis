import csv, sys, re, os
from subprocess import Popen, PIPE

BENCH_LOCATION = "./NPB3.4.1/NPB3.4-OMP/bin/"
BENCH_LIST_OMP = ["bt", "cg", "ep", "ft", "is", "lu", "mg", "sp", "ua", "dc"]
CLASS_LIST_OMP = ["S", "W", "A", "B", "C", "D", "E", "F"]
RESULT_OFFSET = 2

# BENCHES = [
#     'bt.S.x', 'cg.A.x', 'dc.S.x', 'ep.A.x', 'ft.S.x', 'is.S.x', 'lu.S.x', 'mg.S.x', 'sp.S.x', 'ua.S.x',
# ]

BENCHES = [
    'bt.A.x', 'bt.B.x', 'bt.C.x', 'bt.S.x', 'bt.W.x', # 'bt.D.x', 'bt.E.x', 'bt.F.x', 
    'cg.A.x', 'cg.B.x', 'cg.C.x', # 'cg.D.x', 'cg.E.x', 'cg.F.x', 'cg.S.x', 'cg.W.x',
    'dc.A.x', 'dc.B.x', 'dc.S.x', 'dc.W.x',
    'ep.A.x', 'ep.B.x', 'ep.C.x', 'ep.D.x', # 'ep.E.x', 'ep.F.x', 'ep.S.x', 'ep.W.x',
    'ft.A.x', 'ft.B.x', 'ft.C.x', 'ft.S.x', 'ft.W.x', # 'ft.D.x', 'ft.E.x', 'ft.F.x', 
    'is.A.x', 'is.B.x', 'is.C.x', 'is.S.x', 'is.W.x',
    'lu.A.x', 'lu.B.x', 'lu.C.x', 'lu.S.x', 'lu.W.x', # 'lu.D.x', 'lu.E.x', 'lu.F.x', 
    'mg.A.x', 'mg.B.x', 'mg.C.x', 'mg.D.x', 'mg.S.x', 'mg.W.x', # 'mg.E.x', 'mg.F.x', 
    'sp.A.x', 'sp.B.x', 'sp.C.x', 'sp.S.x', 'sp.W.x', # 'sp.D.x', 'sp.E.x', 'sp.F.x', 
    'ua.A.x', 'ua.B.x', 'ua.C.x', 'ua.S.x', 'ua.W.x', # 'ua.D.x', 
]

INDEX_EVENT = 0
INDEX_NAME  = 2

INDEX_RESULT = 0
INDEX_EVENT_NAME = 1
INDEX_OTHERS = 2
INDEX_CLOCK_OTHERS = 1

PATTERN_HEADER = "Performance counter stats for"
PATTERN_FOOTER = "seconds time elapsed"
PATTERN = "(" + PATTERN_HEADER + ")(.)*(" + PATTERN_FOOTER + ")"
pattern = re.compile(PATTERN, re.DOTALL)

def usage():
    print("usage: python3 ./run_benchmarks [input_file] [output_file] [num_of_concurrent_events] [iteration]")
    exit()

def run_bench_get_stdout(benchmark, events):
    process = Popen(
        ["perf", "stat", "-e", events, "taskset", "-c", "0-15", benchmark],
        stdout=PIPE, stderr=PIPE,
    )

    # process = Popen(
    #     ["perf", "stat", "-e", events, "-I", interval, "-a", benchmark],
    #     stdout=PIPE, stderr=PIPE,
    # )

    (_, perf_result) = process.communicate()
    process.communicate()
    process.wait()
    result = perf_result.decode("utf-8")
    print(result)
    return result

def concat_events(event_list):
    concated = ""
    for event in event_list[:-1]:
        concated += (event + ",")
    return concated + event_list[-1]

def to_num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def get_bench_results(bench_name, events, iteration):
    m = pattern.search(run_bench_get_stdout(BENCH_LOCATION + bench_name, events))
    if m is not None:
        split_lines = m.group().splitlines()
        bench_result = [l.split('  ') for l in split_lines[2:-2] + [split_lines[-1]]]
        bench_result_cut = []
        for line in bench_result:
            new_line = [
                item for item in [item.strip() for item in line] if len(item) > 0 and item != "#"
            ]
            len_new_line = len(new_line)
            if len_new_line == 1:
                if new_line[0][-7:] == "elapsed":
                    split = new_line[INDEX_RESULT].split()
                    new_line = [
                        "time-elapsed ({0})".format(iteration), split[0], split[1]
                    ]
            elif len_new_line > 1:
                if new_line[0][-5:] == "clock":
                    split = new_line[INDEX_RESULT].split()
                    new_line = [
                        split[-1], split[0],
                        "msec"
                    ] + new_line[INDEX_CLOCK_OTHERS:]
                else:
                    new_line = [
                        new_line[INDEX_EVENT_NAME], new_line[INDEX_RESULT]
                    ] + new_line[INDEX_OTHERS:]
            new_line = [str(iteration), bench_name] + new_line
            bench_result_cut.append(new_line)
        # print(bench_result_cut)
        return bench_result_cut
    else:
        print("None")
        return None

def run_benchs(input_file, result_file, num_of_concurrent_events, iteration):
    with open(input_file, 'r') as fr, open(result_file, 'w', newline='') as fw:
        reader_list = [l for l in csv.reader(fr)][1:]
        events = [line[INDEX_EVENT] for line in reader_list]
        event_names = [line[INDEX_NAME] for line in reader_list]

        # write header
        writer = csv.writer(fw)
        writer.writerow(["iteration", "bench_name", "event", "result"])

        # run benchs
        for it in range(1, iteration+1):
            for bench_name in BENCHES:
                event_groups_num = len(event_names)//num_of_concurrent_events + 1 \
                    if len(event_names) % num_of_concurrent_events != 0 \
                    else len(event_names)//num_of_concurrent_events
                
                for i in range(0, event_groups_num):
                    print("Iteration {0}/{1}: run benchmark {2} ({3}/{4})".format(
                            it, iteration, bench_name, i+1, event_groups_num
                        )
                    )
                    events_slice = concat_events(
                        events[i*num_of_concurrent_events:(i+1)*num_of_concurrent_events]
                    )
                    writer.writerows(get_bench_results(bench_name, events_slice, it))
            os.system("rm /home/jihyo/ADC.*")
        print("done!")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
    
    # usage: python3 ./run_benchmarks [input_file] [output_file] [num_of_concurrent_events] [iteration]

    num_of_concurrent_events = 0
    try:
        num_of_concurrent_events = int(sys.argv[3])
        iteration                = int(sys.argv[4])
        if num_of_concurrent_events <= 0 or iteration <= 0:
            usage()
    except ValueError:
        usage()

    run_benchs(sys.argv[1], sys.argv[2], num_of_concurrent_events, iteration)

# python3 run_benchmarks.py ./intel_events_cache2_codes.csv ./intel_result.csv 20 10
# python3 run_benchmarks.py ./amd_events_cache_codes.csv ./amd_result.csv 20 10
