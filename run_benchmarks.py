import csv, sys, re, os
from subprocess import Popen, PIPE
# from statistics import mean, stdev

BENCH_LOCATION = "./NPB3.4.1/NPB3.4-OMP/bin/"
BENCH_LIST_OMP = ["bt", "cg", "ep", "ft", "is", "lu", "mg", "sp", "ua", "dc"]
# BENCH_LIST_OMP = ["bt"]
CLASS_LIST_OMP = ["S", "W", "A", "B", "C", "D", "E", "F"]
# CLASS_LIST_OMP = ["S", "W", "A", "B", "C", "D"]
# CLASS_LIST_OMP = ["B"]
HEADER_BASE = ["bench_name", "event"]
# HEADER_BASE2 = ["average", "stddev"]
RESULT_OFFSET = 2

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

# BENCHES = [
#     'bt.A.x', 'bt.S.x', 'bt.W.x', # 'bt.D.x', 'bt.E.x', 'bt.F.x', 'bt.C.x', 'bt.B.x', 
#     'cg.S.x', 'cg.W.x', 'cg.A.x', # 'cg.B.x', #'cg.C.x', # 'cg.D.x', 'cg.E.x', 'cg.F.x',
#     'dc.A.x', 'dc.S.x', 'dc.W.x', # 'dc.B.x', 
#     'ep.S.x', 'ep.W.x', 'ep.A.x', 'ep.B.x', # 'ep.C.x', #'ep.D.x', # 'ep.E.x', 'ep.F.x', 
#     'ft.A.x', 'ft.B.x', 'ft.S.x', 'ft.W.x', # 'ft.D.x', 'ft.E.x', 'ft.F.x', 'ft.C.x', 
#     'is.A.x', 'is.B.x', 'is.S.x', 'is.W.x', # 'is.C.x', 
#     'lu.A.x', 'lu.B.x', 'lu.S.x', 'lu.W.x', # 'lu.D.x', 'lu.E.x', 'lu.F.x', 
#     'mg.A.x', 'mg.B.x', 'mg.S.x', 'mg.W.x', # 'mg.E.x', 'mg.F.x', 'mg.D.x', 'mg.C.x', 
#     'sp.A.x', 'sp.B.x', 'sp.S.x', 'sp.W.x', # 'sp.D.x', 'sp.E.x', 'sp.F.x', 'sp.C.x', 
#     'ua.A.x', 'ua.B.x', 'ua.S.x', 'ua.W.x', # 'ua.D.x', 'ua.C.x', 
# ]

# BENCHES = [
#     'bt.A.x', 'bt.S.x', 'bt.W.x', # 'bt.D.x', 'bt.E.x', 'bt.F.x', 'bt.C.x', 'bt.B.x', 
#     'cg.S.x', 'cg.W.x', 'cg.A.x', # 'cg.B.x', #'cg.C.x', # 'cg.D.x', 'cg.E.x', 'cg.F.x',
#     'dc.A.x', 'dc.S.x', 'dc.W.x', # 'dc.B.x', 
#     'ep.S.x', 'ep.W.x', 'ep.A.x', 'ep.B.x', # 'ep.C.x', #'ep.D.x', # 'ep.E.x', 'ep.F.x', 
#     'ft.A.x', 'ft.B.x', 'ft.S.x', 'ft.W.x', # 'ft.D.x', 'ft.E.x', 'ft.F.x', 'ft.C.x', 
#     'is.A.x', 'is.B.x', 'is.S.x', 'is.W.x', # 'is.C.x', 
#     'lu.A.x', 'lu.B.x', 'lu.S.x', 'lu.W.x', # 'lu.D.x', 'lu.E.x', 'lu.F.x', 
#     'mg.A.x', 'mg.B.x', 'mg.C.x', 'mg.S.x', 'mg.W.x', # 'mg.E.x', 'mg.F.x', 'mg.D.x',  
#     'sp.A.x', 'sp.B.x', 'sp.C.x', 'sp.S.x', 'sp.W.x', # 'sp.D.x', 'sp.E.x', 'sp.F.x',  
#     'ua.A.x', 'ua.B.x', 'ua.S.x', 'ua.W.x', # 'ua.D.x', 'ua.C.x', 
# ]

INDEX_EVENT = 0
INDEX_NAME  = 2

PATTERN_HEADER = "Performance counter stats for 'system wide':"
PATTERN_FOOTER = "seconds time elapsed"
PATTERN = "(" + PATTERN_HEADER + ")(.)*(" + PATTERN_FOOTER + ")"
pattern = re.compile(PATTERN, re.DOTALL)

def usage():
    print("usage: python3 ./run_benchmarks [input_file] [output_file] [num_of_concurrent_events] [interval]")
    exit()

def run_bench_get_stdout(benchmark, events, interval):
    # arr = ["perf", "stat", "-e", events, "-a", benchmark]
    # print(" ".join(arr))

    process = Popen(
        ["perf", "stat", "-e", events, "-a", benchmark],
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
    # print(result)
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

def get_bench_results(benchmark, events, interval):



    # bench_result = [
    #     j.split('  ') for j in
    #         [
    #             i for i in run_bench_get_stdout(benchmark, events, interval).splitlines()
    #                 if len(i) > 0
    #         ]
    #         if j[0] != '#'
    # ]

    # fn_result = {}
    # for stat in bench_result:
    #     if stat[0] == '<not':
    #         fn_result[stat[2]] = ['<not supported>']
    #     else:
    #         if stat[1] in fn_result:
    #             # fn_result[stat[1]].append(to_num(stat[0].replace(',','')))
    #             fn_result[stat[1]].append(stat)
    #         else:
    #             # fn_result[stat[1]] = [to_num(stat[0].replace(',',''))]
    #             fn_result[stat[1]] = stat
    # # print(fn_result)
    # return fn_result

    # bench_result = []
    m = pattern.search(run_bench_get_stdout(benchmark, events))
    if m is not None:
        bench_result = [l.split('  ') for l in m.group().splitlines()[2:-2] if len(l) > 1]
        print(bench_result)
    else:
        print("pattern not match.")

    # fn_result = {}
    # for stat in bench_result:
    #     if stat[0] == '<not':
    #         fn_result[stat[2]] = stat[0] + ' ' + stat[1]
    #     else:
    #         fn_result[stat[1]] = to_num(stat[0].replace(',',''))

    # return fn_result

def run_benchs(input_file, result_file, num_of_concurrent_events, interval):
    with open(input_file, 'r') as fr, open(result_file, 'w', newline='') as fw:
        # write header
        # header = HEADER_BASE + ["iter"+str(i) for i in range(1, iteration+1)] # + HEADER_BASE2
        writer = csv.writer(fw)
        # writer.writerow(header)
        writer.writerow(HEADER_BASE + ['result'])
        
        reader_list = [l for l in csv.reader(fr)][1:]
        events = [line[INDEX_EVENT] for line in reader_list]
        event_names = [line[INDEX_NAME] for line in reader_list]

        # run benchs
        # bench_list = []
        # for bench in BENCH_LIST_OMP:
        #     for cls in CLASS_LIST_OMP:
        #         bench_list.append(bench + "." + cls + ".x")

        # bench_list = os.listdir(BENCH_LOCATION)
        # bench_list.sort()
        # for bench_name in bench_list:
        for bench_name in BENCHES:
            benchmark = BENCH_LOCATION + bench_name
            results = [[bench_name, event_name] for event_name in event_names]
            
            event_groups_num = len(event_names)//num_of_concurrent_events + 1 \
                if len(event_names) % num_of_concurrent_events != 0 \
                else len(event_names)//num_of_concurrent_events
            
            for i in range(0, event_groups_num):
                print("run benchmark {0} ({1}/{2})".format(bench_name, i+1, event_groups_num))
                events_slice = concat_events(
                    events[i*num_of_concurrent_events:(i+1)*num_of_concurrent_events]
                )

                bench_result = get_bench_results(benchmark, events_slice, interval)
                for line in results:
                    if line[1] in bench_result:
                        line += bench_result[line[1]]

                # for i in range(1, iteration+1):
                #     print("run {0}, iteration: {1}".format(bench_name, i))
                #     begin, end = 0, 0
                #     while(begin < len(event_names)):
                #         end = begin + num_of_events
                #         events_slice = concat_events(events[begin:end])

                #         bench_result = get_bench_results(benchmark, events_slice)
                #         for line in results:
                #             if line[1] in bench_result:
                #                 line.append(bench_result[line[1]])

                #         begin = end

            writer.writerows(results)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        usage()
    
    # usage: python3 ./run_benchmarks [input_file] [output_file] [num_of_concurrent_events] [interval]

    num_of_concurrent_events = 0
    try:
        num_of_concurrent_events = int(sys.argv[3])
        iteration                = int(sys.argv[4])
        if num_of_concurrent_events <= 0 or iteration <= 0:
            usage()
    except ValueError:
        usage()

    run_benchs(sys.argv[1], sys.argv[2], num_of_concurrent_events, sys.argv[4])

# python3 run_benchmarks.py ./intel_events_cache2_codes.csv ./intel_result.csv 20 100
# python3 run_benchmarks.py ./amd_events_cache_codes.csv ./amd_result.csv 20 100
