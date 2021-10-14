import csv, re
from subprocess import Popen, PIPE

PMU_NAME = {
    'amd64_fam15h_interlagos (AMD64 Fam15h Interlagos)'  : 'cpu',
    'amd64_fam15h_nb (AMD64 Fam15h NorthBridge)'         : 'amd_nb',
    'hsw_ep (Intel Haswell EP)'                          : 'cpu',
    'ix86arch (Intel X86 architectural PMU)'             : 'cpu',
    'hswep_unc_cbo0 (Intel Haswell-EP C-Box 0 uncore)'   : 'uncore_cbox_0',
    'hswep_unc_cbo1 (Intel Haswell-EP C-Box 1 uncore)'   : 'uncore_cbox_1',
    'hswep_unc_cbo2 (Intel Haswell-EP C-Box 2 uncore)'   : 'uncore_cbox_2',
    'hswep_unc_cbo3 (Intel Haswell-EP C-Box 3 uncore)'   : 'uncore_cbox_3',
    'hswep_unc_cbo4 (Intel Haswell-EP C-Box 4 uncore)'   : 'uncore_cbox_4',
    'hswep_unc_cbo5 (Intel Haswell-EP C-Box 5 uncore)'   : 'uncore_cbox_5',
    'hswep_unc_cbo6 (Intel Haswell-EP C-Box 6 uncore)'   : 'uncore_cbox_6',
    'hswep_unc_cbo7 (Intel Haswell-EP C-Box 7 uncore)'   : 'uncore_cbox_7',
    'hswep_unc_cbo8 (Intel Haswell-EP C-Box 8 uncore)'   : 'uncore_cbox_8',
    'hswep_unc_cbo9 (Intel Haswell-EP C-Box 9 uncore)'   : 'uncore_cbox_9',
    'hswep_unc_cbo10 (Intel Haswell-EP C-Box 10 uncore)' : 'uncore_cbox_10',
    'hswep_unc_cbo11 (Intel Haswell-EP C-Box 11 uncore)' : 'uncore_cbox_11',
    'hswep_unc_cbo12 (Intel Haswell-EP C-Box 12 uncore)' : 'uncore_cbox_12',
    'hswep_unc_cbo13 (Intel Haswell-EP C-Box 13 uncore)' : 'uncore_cbox_13',
    'hswep_unc_cbo14 (Intel Haswell-EP C-Box 14 uncore)' : 'uncore_cbox_14',
    'hswep_unc_cbo15 (Intel Haswell-EP C-Box 15 uncore)' : 'uncore_cbox_15',
    'hswep_unc_cbo16 (Intel Haswell-EP C-Box 16 uncore)' : 'uncore_cbox_16',
    'hswep_unc_cbo17 (Intel Haswell-EP C-Box 17 uncore)' : 'uncore_cbox_17',
    'hswep_unc_ha0 (Intel Haswell-EP HA 0 uncore)'       : 'uncore_ha_0',
    'hswep_unc_ha1 (Intel Haswell-EP HA 1 uncore)'       : 'uncore_ha_1',
    'hswep_unc_qpi0 (Intel Haswell-EP QPI0 uncore)'      : 'uncore_qpi_0',
    'hswep_unc_qpi1 (Intel Haswell-EP QPI1 uncore)'      : 'uncore_qpi_1',
    'hswep_unc_sbo0 (Intel Haswell-EP S-BOX0 uncore)'    : 'uncore_sbox_0',
    'hswep_unc_sbo1 (Intel Haswell-EP S-BOX1 uncore)'    : 'uncore_sbox_1',
    'hswep_unc_sbo2 (Intel Haswell-EP S-BOX2 uncore)'    : 'uncore_sbox_2',
    'hswep_unc_sbo3 (Intel Haswell-EP S-BOX3 uncore)'    : 'uncore_sbox_3',

}
PROGRAM_NAME = "./libpfm-4.11.0/examples/check_events"
INDEX_IDX   = 0
INDEX_PMU  = 1
INDEX_NAME = 2
INDEX_EQUIV  = 3
INDEX_FLAGS = 4
INDEX_DESC = 5
INDEX_CODE = 6
HEADER = ["Event_code", "PMU", "Name", "Equiv", "Desc"]

CODE_TEXT = "Codes          : "
pattern = re.compile("("+CODE_TEXT+")(.)*")

def fetch_code(event_name):
    process = Popen([PROGRAM_NAME, event_name], stdout=PIPE)
    (output, _) = process.communicate()
    process.wait()
    output_str = output.decode("utf-8")
    # print(output_str[:30])
    s = pattern.search(output_str)
    if s is not None:
        # print("result: {0}".format(s.group().split()))
        return s.group().split()[2:]
    else:
        # print("search result: none")
        return None

def get_event_codes(event_file_name, result_file_name, manufacturer):
    with open(event_file_name, 'r') as fr, open(result_file_name, 'w', newline='') as fw:
        lines = [line for line in csv.reader(fr)]
        writer = csv.writer(fw)
        writer.writerow(HEADER)

        # get the index list of umask
        umask_indices = []
        umask_pattern = re.compile('(Umask-)[1-9]*')
        for index, item in enumerate(lines[0]):
            if umask_pattern.search(item) is not None:
                umask_indices.append(index)
        # print(umask_indices)

        for line in lines[1:]:
            # for PMU events, using the name of event itself would work
            if line[INDEX_PMU] == 'perf (perf_events generic PMU)':
                if line[INDEX_EQUIV] != 'None':
                    writer.writerow(
                        [line[INDEX_NAME], line[INDEX_PMU], line[INDEX_NAME], line[INDEX_EQUIV], line[INDEX_DESC]]
                    )
            else:
                # find PMU from PMU list and get 
                pmu_name = '\"' + PMU_NAME[line[INDEX_PMU]] if line[INDEX_PMU] in PMU_NAME else '\"cpu'
                
                # write a line for each umask in an event
                cnt = 0
                for index in umask_indices:
                    if line[index] != '':
                        umask_code = line[index][:line[index].find(' : ')]
                        umask_name = line[index][line[index].find('[')+1:line[index].find(']')]
                        umask_desc = line[index][line[index].rfind(' : '):]
                        event_name = line[INDEX_NAME] + ":" + umask_name

                        codes = fetch_code(event_name)
                        if manufacturer == "Intel" and codes is None:
                            codes = fetch_code(line[INDEX_NAME])
                            if codes is None:
                                continue

                        if codes is not None:
                            event_code = pmu_name + ("/config=" + codes[0]) \
                                + (",config1=" + codes[1] if len(codes) >= 2 else '') \
                                + (",config2=" + codes[2] if len(codes) == 3 else '')
                            event_code += (
                                '' if manufacturer == "Intel" and line[INDEX_NAME][0:3] != "UNC"
                                else (',umask=' + umask_code)
                            )
                            event_code += (',name=' + event_name + '/\"')

                            writer.writerow(
                                [event_code]
                                + [line[INDEX_PMU], event_name, line[INDEX_EQUIV]]
                                + [line[INDEX_DESC] + umask_desc]
                            )
                            cnt += 1

                # write a line if the event has no umask option
                if cnt == 0:
                    # event += (',name=' + line[INDEX_NAME] + '/\"')
                    codes = fetch_code(line[INDEX_NAME])
                    if codes is not None:    
                        writer.writerow(
                            [pmu_name + "/config=" + codes[0] + (',name=' + line[INDEX_NAME] + '/\"')]
                            + [line[INDEX_PMU], line[INDEX_NAME], line[INDEX_EQUIV], line[INDEX_DESC]]
                        )

if __name__ == '__main__':
    # get_event_codes('./amd_events_cache.csv', './amd_events_cache_codes.csv')
    # get_event_codes('./intel_events_cache2.csv', './intel_events_cache2_codes.csv', 'intel')
    # get_event_codes('./amd_non_ovlp_events.csv', './amd_non_ovlp_codes.csv', "AMD")
    # get_event_codes('./intel_non_ovlp_events.csv', './intel_non_ovlp_codes.csv', 'intel')

    # get_event_codes("../test_omp_thrd16/amd_events.csv", "../test_omp_thrd16/amd_codes.csv", "AMD")
    # get_event_codes("../test_omp_thrd16/intel_events.csv", "../test_omp_thrd16/intel_codes.csv", "intel")

    # get_event_codes("./amd_events_16.csv", "./amd_codes_16.csv", "AMD")
    # get_event_codes("./intel_events_16.csv", "./intel_codes_16.csv", "Intel")
    # get_event_codes("./intel_events_16.csv", "./intel_codes_16.csv", "Intel")

    # get_event_codes("./amd_events_perf.csv", "./amd_codes_perf.csv", "AMD")
    get_event_codes("./intel_events_perf.csv", "./intel_codes_perf.csv", "Intel")

    # fetch_code("MISALIGN_MEM_REF:LOADS")
