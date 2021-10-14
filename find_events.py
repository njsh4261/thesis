import csv, re

def find_events(event_file_name, keyword, result_file_name):
    with open(event_file_name, 'r') as fr, open(result_file_name, 'w', newline='') as fw:
        pattern = re.compile('(.)*(' + keyword + ')(.)*')
        cnt = 0
        writer = csv.writer(fw)
        for line in csv.reader(fr):
            if cnt == 0:
                writer.writerow(line)
                cnt += 1
            else:
                for item in line:
                    if pattern.search(item, re.IGNORECASE) is not None:
                        writer.writerow(line)
                        cnt += 1
                        break

if __name__ == '__main__':
    # find_events('../amd_events.csv', 'cache|CACHE', '../amd_events_cache.csv')
    # find_events('../intel_events.csv', 'cache|CACHE', '../intel_events_cache.csv')
    find_events('../amd_events.csv', 'cache|Cache|CACHE|L1|L2|L3|LLC|TLB', '../test_omp_thrd16/amd_events_shifted.csv')
    find_events('../intel_events.csv', 'cache|Cache|CACHE|L1|L2|L3|LLC|TLB', '../test_omp_thrd16/intel_events_shifted.csv')
