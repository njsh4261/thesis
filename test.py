import re
from subprocess import Popen, PIPE

PATTERN_HEADER = "Performance counter stats for 'system wide':"
PATTERN_FOOTER = "seconds time elapsed"
PATTERN = "(" + PATTERN_HEADER + ")(.)*(" + PATTERN_FOOTER + ")"
pattern = re.compile(PATTERN, re.DOTALL)
events = "cpu-cycles,instructions,cache-references,cache-misses,branch-instructions,branch-misses,bus-cycles,stalled-cycles-frontend,stalled-cycles-backend,ref-cycles,cpu-clock,task-clock,page-faults,context-switches,cpu-migrations,minor-faults,major-faults,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-dcache-store-misses,L1-dcache-prefetches,L1-dcache-prefetch-misses,L1-icache-loads,L1-icache-load-misses,L1-icache-prefetches,L1-icache-prefetch-misses,LLC-loads,LLC-load-misses"

process = Popen(
    ["perf", "stat", "-e", events, "-a", "./NPB3.4.1/NPB3.4-OMP/bin/mg.A.x"],
    stdout=PIPE, stderr=PIPE,
)

(_, perf_result) = process.communicate()
process.communicate()
process.wait()
result = perf_result.decode("utf-8")


m = pattern.search(result)
if m is not None:
    bench_result = [l.split('  ') for l in m.group().splitlines()[2:-2]]
    for line in bench_result:
        line = [item.strip() for item in line if item not in ["", " "]]
        print(line)
else:
    print("pattern not match.")