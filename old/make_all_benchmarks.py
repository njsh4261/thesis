import os

BENCH_LIST_MPI = []
CLASS_LIST_MPI = []
BENCH_LIST_OMP = ["bt", "cg", "ep", "ft", "is", "lu", "mg", "sp", "ua", "dc"]
CLASS_LIST_OMP = ["S", "W", "A", "B", "C", "D", "E", "F"]

def make_all(path, bench_list, class_list):
    for b in bench_list:
        for c in class_list:
            os.system("make -C " + path + ' ' + b + ' CLASS=' + c)

if __name__ == '__main__':
    make_all('./NPB3.4.1/NPB3.4-OMP', BENCH_LIST_OMP, CLASS_LIST_OMP)
    # make_all('./NPB3.4.1/NPB3.4-MPI', BENCH_LIST_MPI, CLASS_LIST_MPI)