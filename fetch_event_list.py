import csv

def get_event_infos(file_name):
    result = []
    header_list = []
    with open(file_name, 'r') as f:
        cnt = 0
        for line in f.readlines():
            if line == "#-----------------------------\n":
                cnt += 1
                result.append({})
            else:
                if cnt == 0:
                    continue
                else:
                    attribute = line[0:line.find(' ')].strip().replace('\t','')
                    item = line[line.find(' : ')+3:]
                    if not attribute in header_list:
                        header_list.append(attribute)
                    result[cnt-1][attribute] = item.strip().replace('\t','')
    return result, header_list

def write_csv_file(event_list, header_list, new_file_name):
    with open(new_file_name, 'w', newline='') as f:
        writer = csv.writer(f)

        # get and write header first
        writer.writerow(header_list)

        # write events
        for row_item in event_list:
            row = []
            for header_item in header_list:
                if header_item in row_item:
                    row.append(row_item[header_item])
                else:
                    row.append('')
            writer.writerow(row)


def main():
    # make AMD list
    amd_list, amd_header_list = get_event_infos('../amd_show_event_info.txt')
    write_csv_file(amd_list, amd_header_list, '../amd_events.csv')

    # make Intel list
    intel_list, intel_header_list = get_event_infos('../intel_show_event_info.txt')
    write_csv_file(intel_list, intel_header_list, '../intel_events.csv')

if __name__ == '__main__':
    main()