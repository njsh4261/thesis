import csv

def non_overlapping(input1, input2, output):
    with open(input1, 'r') as f1, open(input2, 'r') as f2, open(output, 'w', newline='') as f3:
        list_existing = [l for l in csv.reader(f2)]
        writer = csv.writer(f3)
        writer.writerow(list_existing[0])

        for l in csv.reader(f1):
            if l not in list_existing:
                writer.writerow(l)

if __name__ == '__main__':
    non_overlapping('../amd_events_shifted.csv', '../amd_events_cache.csv', '../amd_non_ovlp_events.csv')
    non_overlapping('../intel_events_shifted.csv', '../intel_events_cache2.csv', '../intel_non_ovlp_events.csv')
    