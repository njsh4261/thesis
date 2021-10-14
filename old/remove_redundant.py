import csv

# intel: 총 152750행, 47개 벤치마크의 결과 3250개 중 마지막 250개만 유용
# AMD: 총 60160행, 47개 벤치마크의 결과 1280개 중 마지막 160개만 유용

def remove_redundant(input, output):
    with open(input, 'r') as fr, open(output, 'w', newline='') as fw:
        print("{0} -> {1} ...".format(input, output), end=' ')
        lines = [line for line in csv.reader(fr)]
        writer = csv.writer(fw)
        writer.writerow(lines[0])

        result = []
        for line in lines[1:]:
            line = [i for i in line if i != '']
            if len(line) > 2:
                if line not in result:
                    if line[2] != '<not supported>':
                        result.append(line)
        writer.writerows(result)
        print("done!")

if __name__ == "__main__":
    # remove_redundant("../result/intel_result.csv", "../result/intel_result_cut.csv")
    # remove_redundant("../result/amd_result.csv", "../result/amd_result_cut.csv")
    remove_redundant("../result/amd_result_ovlp.csv", "../result/amd_result_ovlp_cut.csv")
