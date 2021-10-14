import csv, re
import numpy as np
from numpy.lib.function_base import percentile
from scipy import stats
from scipy.stats.stats import trim_mean

HEADER = [
    "벤치마크 이름", "이벤트 이름",
    "표본수", "평균", "절사평균", "표준편차",
    "최대값", "1분위수", "중간값", "3분위수", "최소값",
    "결과 데이터"
]

def get_statistics(input, output):
    # int_pattern = re.compile("(\d)*")
    # float_pattern = re.compile("(\d)*(\.)(\d)*")

    with open(input, 'r') as fr, open(output, 'w', newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow(HEADER)

        # for line in [l for l in csv.reader(fr)][1:]:
        #     for i in line[2:]:
        #         if int_pattern.match(i) is None:
        #             print("int match failed at '{}'.".format(i))
        #             exit()
        #         if float_pattern.match(i) is not None:
        #             print("float item found at '{}'.".format(i))
        #             exit()
        # print("all items can be converted to int.")

        for line in [l for l in csv.reader(fr)][1:]:
            bench_event = line[:2]
            data = np.array(line[2:], dtype=np.float64)
            quartile = np.percentile(data, [100, 75, 50, 25, 0], interpolation='nearest')
            stat = [
                data.size,
                np.mean(data),
                stats.trim_mean(data, 0.2),
                np.std(data),
            ] + quartile.tolist()
            writer.writerow(bench_event + stat + line[2:])

if __name__ == "__main__":
    # get_statistics("../result/intel_result_cut.csv", "../result/intel_result_stat.csv")
    # get_statistics("../result/amd_result_cut.csv", "../result/amd_result_stat.csv")
    get_statistics("../result/amd_result_ovlp_cut.csv", "../result/amd_result_stat2.csv")
