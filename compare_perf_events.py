import csv

HEADER = [
    "벤치마크 이름", "이벤트 이름",
    "AMD 인터벌 수", "인텔 인터벌 수", "실행시간의 비율",
    "AMD 평균", "인텔 평균", "평균의 비율",
]
OFFSET = 2

def csv_to_dict(fd):
    result = {}
    for l in [l for l in csv.reader(fd)][1:]:
        result[(l[0], l[1])] = l[2:]
    return result

def compare_events(input1, input2, output):
    with open(input1, 'r') as f1, open(input2, 'r') as f2, \
        open(output, 'w', newline='') as f3:
        writer = csv.writer(f3)
        writer.writerow(HEADER)

        events1 = csv_to_dict(f1)
        for l in csv.reader(f2):
            key = (l[0], l[1])
            if key in events1:
                writer.writerow(
                    l[0:2] + [
                        events1[key][2-OFFSET], l[2],
                        float(l[2]) / float(events1[key][2-OFFSET]), # intervals
                        events1[key][3-OFFSET], l[3],
                        float(l[3]) / float(events1[key][3-OFFSET]), # means
                    ]
                )

if __name__ == '__main__':
    compare_events(
        "../result/amd_result_stat.csv",
        "../result/intel_result_stat.csv",
        "../result/perf_compare.csv"
    )