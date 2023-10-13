from triage import *

# (target bin, target cmdline, input src, additional option, triage function)
#check_Binary_CVEnum은 실제 해당 CVE가 맞는지 확인하는 triage
FUZZ_TARGETS = [
    ("swftophp-4.7-2016-9827", "@@", "file", check_swftophp_2016_9827),
    ("swftophp-4.7-2016-9829", "@@", "file", check_swftophp_2016_9829),
    ("swftophp-4.7-2016-9831", "@@", "file", check_swftophp_2016_9831),
    ("swftophp-4.7-2017-9988", "@@", "file", check_swftophp_2017_9988),
    ("swftophp-4.7-2017-11728", "@@", "file", check_swftophp_2017_11728),
    ("swftophp-4.7-2017-11729", "@@", "file", check_swftophp_2017_11729),
    ("swftophp-4.7-2017-7578", "@@", "file", check_swftophp_2017_7578),
    ("swftophp-4.8-2018-7868", "@@", "file", check_swftophp_2018_7868),
    ("swftophp-4.8-2018-8807", "@@", "file", check_swftophp_2018_8807),
    ("swftophp-4.8-2018-8962", "@@", "file", check_swftophp_2018_8962),
    ("swftophp-4.8-2018-11095", "@@", "file", check_swftophp_2018_11095),
    ("swftophp-4.8-2018-11225", "@@", "file", check_swftophp_2018_11225),
    ("swftophp-4.8-2018-11226", "@@", "file", check_swftophp_2018_11226),
    ("swftophp-4.8-2018-20427", "@@", "file", check_swftophp_2018_20427),
    ("swftophp-4.8-2019-9114", "@@", "file", check_swftophp_2019_9114),
    ("swftophp-4.8-2019-12982", "@@", "file", check_swftophp_2019_12982),
    ("swftophp-4.8-2020-6628", "@@", "file", check_swftophp_2020_6628),
    ("cxxfilt-2016-4487", "", "stdin", check_cxxfilt_2016_4487),
    ("cxxfilt-2016-4489", "", "stdin", check_cxxfilt_2016_4489),
    ("cxxfilt-2016-4490", "", "stdin", check_cxxfilt_2016_4490),
    ("cxxfilt-2016-4491", "", "stdin", check_cxxfilt_2016_4491),
    ("cxxfilt-2016-4492", "", "stdin", check_cxxfilt_2016_4492),
    ("cxxfilt-2016-6131", "", "stdin", check_cxxfilt_2016_6131),
    ("objdump-2017-8396", "-W @@", "file", check_objdump_2017_8396),
    ("objdump-2017-8397", "-W @@", "file", check_objdump_2017_8397),
    ("objdump-2017-8398", "-W @@", "file", check_objdump_2017_8398),
]

 
SWFTOPHP47_TARGETS = [
    ("swftophp-4.7-2016-9827", "@@", "file", check_swftophp_2016_9827),
    ("swftophp-4.7-2016-9829", "@@", "file", check_swftophp_2016_9829),
    ("swftophp-4.7-2016-9831", "@@", "file", check_swftophp_2016_9831),
    ("swftophp-4.7-2017-9988", "@@", "file", check_swftophp_2017_9988),
    ("swftophp-4.7-2017-11728", "@@", "file", check_swftophp_2017_11728),
    ("swftophp-4.7-2017-11729", "@@", "file", check_swftophp_2017_11729),
    ("swftophp-4.7-2017-7578", "@@", "file", check_swftophp_2017_7578),
]

SWFTOPHP48_TARGETS = [
    ("swftophp-4.8-2018-7868", "@@", "file", check_swftophp_2018_7868),
    ("swftophp-4.8-2018-8807", "@@", "file", check_swftophp_2018_8807),
    ("swftophp-4.8-2018-8962", "@@", "file", check_swftophp_2018_8962),
    ("swftophp-4.8-2018-11095", "@@", "file", check_swftophp_2018_11095),
    ("swftophp-4.8-2018-11225", "@@", "file", check_swftophp_2018_11225),
    ("swftophp-4.8-2018-11226", "@@", "file", check_swftophp_2018_11226),
    ("swftophp-4.8-2018-20427", "@@", "file", check_swftophp_2018_20427),
    ("swftophp-4.8-2019-9114", "@@", "file", check_swftophp_2019_9114),
    ("swftophp-4.8-2019-12982", "@@", "file", check_swftophp_2019_12982),
    ("swftophp-4.8-2020-6628", "@@", "file", check_swftophp_2020_6628)
]

CXXFILT_TARGETS = [
    ("cxxfilt-2016-4487", "", "stdin", check_cxxfilt_2016_4487),
    ("cxxfilt-2016-4489", "", "stdin", check_cxxfilt_2016_4489),
    ("cxxfilt-2016-4490", "", "stdin", check_cxxfilt_2016_4490),
    ("cxxfilt-2016-4491", "", "stdin", check_cxxfilt_2016_4491),
    ("cxxfilt-2016-4492", "", "stdin", check_cxxfilt_2016_4492),
    ("cxxfilt-2016-6131", "", "stdin", check_cxxfilt_2016_6131),
]

OBJDUMP_TARGETS = [
    ("objdump-2017-8396", "-W @@", "file", check_objdump_2017_8396),
    ("objdump-2017-8397", "-W @@", "file", check_objdump_2017_8397),
    ("objdump-2017-8398", "-W @@", "file", check_objdump_2017_8398),
]


def generate_fuzzing_worklist(benchmark, iteration):
    worklist = []
    if benchmark == "swftophp-4.7":
        target_list = SWFTOPHP47_TARGETS
    elif benchmark == "swftophp-4.8":
        target_list = SWFTOPHP48_TARGETS        
    elif benchmark == "cxxfilt":
        target_list = CXXFILT_TARGETS
    elif benchmark == "objdump":
        target_list = OBJDUMP_TARGETS
    else:
        print("++++++++++++++++++ [ERROR] benchmark.py : program if +++++++++++++++")

    for (targ_prog, cmdline, src, _) in TARGETS:
        # if src not in ["stdin", "file", "-@@"]:
        #     print("Invalid input source specified: %s" % src)
        #     exit(1)
        for i in range(iteration):
            iter_id = "iter-%d" % i
            worklist.append((targ_prog, cmdline, src, iter_id))

    return worklist


def check_targeted_crash(targ, replay_buf):

    for (targ_prog, _, _, crash_checker) in FUZZ_TARGETS:
        if targ_prog == targ:
            return crash_checker(replay_buf)
    print("Unknown target: %s" % targ)
    exit(1)
