import sys, os, time, csv, shutil
from common import run_cmd, run_cmd_in_docker, check_cpu_count, fetch_works, MEM_PER_INSTANCE
from benchmark import generate_fuzzing_worklist, FUZZ_TARGETS
from parse_result import print_result
import copy

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
IMAGE_NAME = "edenseo/recfuzz"
SUPPORTED_TOOLS = \
  ["Recfuzz", ]


def decide_outdir(target, timelimit, iteration, tool):
    name = "%s-%ssec-%siters" % (target, timelimit, iteration)
    if target == "origin":
        outdir = os.path.join(BASE_DIR, "output", "origin")
    elif tool == "":
        outdir = os.path.join(BASE_DIR, "output", name)
    else:
        outdir = os.path.join(BASE_DIR, "output", name, tool)
    os.makedirs(outdir, exist_ok=True)
    return outdir


def spawn_containers(works):
    for i in range(len(works)):
        targ_prog, _, _, iter_id = works[i]
        cmd = "docker run --user root --tmpfs /box:exec --rm -m=%dg --cpuset-cpus=%d -it -d --name %s-%s %s" \
                % (MEM_PER_INSTANCE, i, targ_prog, iter_id, IMAGE_NAME)
        run_cmd(cmd)


def run_fuzzing(works, tool, timelimit):
    for (targ_prog, cmdline, src, iter_id) in works:
        cmd = "/tool-script/run_%s.sh %s \"%s\" %s %d > recfuzz.out" % \
                (tool, targ_prog, cmdline, src, timelimit)
        run_cmd_in_docker("%s-%s" % (targ_prog, iter_id), cmd, True)


def wait_finish(works, timelimit):
    time.sleep(timelimit)
    total_count = len(works)
    elapsed_min = 0
    while True:
        if elapsed_min > 30:
            break
        time.sleep(60)
        elapsed_min += 1
        print("Waited for %d min" % elapsed_min)
        finished_count = 0
        for (targ_prog, _, _, iter_id) in works:
            container = "%s-%s" % (targ_prog, iter_id)
            stat_str = run_cmd_in_docker(container, "cat /STATUS", False)
            if "FINISHED" in stat_str:
                finished_count += 1
            else:
                print("%s-%s not finished" % (targ_prog, iter_id))
        if finished_count == total_count:
            print("All works finished!")
            break


def store_outputs(works, outdir):
    for (targ_prog, _, _, iter_id) in works:
        container = "%s-%s" % (targ_prog, iter_id)
        cmd = "docker cp %s:/output %s/%s" % (container, outdir, container)
        #run_cmd(cmd)
        os.system(cmd)



def cleanup_containers(works):
    for (targ_prog, _, _, iter_id) in works:
        cmd = "docker kill %s-%s" % (targ_prog, iter_id)
        run_cmd(cmd)


def main():
    if len(sys.argv) < 4:
        print("Usage: %s <run/parse> <table/figure/target name> <time> <iterations> \"<tool list>\" " % sys.argv[0])
        exit(1)

    check_cpu_count()

    action = sys.argv[1]
    if action not in ["run", "parse"]:
        print("Invalid action! Choose from [run, parse]" )
        exit(1)

    target = sys.argv[2]
    timelimit = int(sys.argv[3])
    iteration = int(sys.argv[4])
    target_list = ""
    tools_to_run = tools = []
    
    if "tbl2" in target:
        benchmark = "all" #tbl2
        target_list = [x for (x,y,z,w) in FUZZ_TARGETS]
        tools += ["Recfuzz"]
    elif target in [x for (x,y,z,w) in FUZZ_TARGETS]:
        benchmark = target 
        target_list = [target]
        if len(sys.argv) == 6:
            tools += sys.argv[5].split()
            if not all([x in SUPPORTED_TOOLS for x in tools]):
                print("Invalid tool in the list! Choose from %s" % SUPPORTED_TOOLS)
                exit(1)
        else:
            tools += SUPPORTED_TOOLS
    else:
        print("Invalid target!")

    ### 1. Run fuzzing
    if action == "run":
        for tool in tools_to_run:
            worklist = generate_fuzzing_worklist(benchmark, iteration)
            outdir = decide_outdir(target, str(timelimit), str(iteration), tool)
            while len(worklist) > 0:
                works = fetch_works(worklist)

                spawn_containers(works) 
                run_fuzzing(works, tool, timelimit) 
                wait_finish(works, timelimit) 
                store_outputs(works, outdir)
                #cleanup_containers(works)
                
                #### Reset timelimit to user input
                timelimit = int(sys.argv[3])

    if "origin" in sys.argv[2]:
        outdir = decide_outdir("origin", "", "", "")
    else:
        outdir = decide_outdir(target, str(timelimit), str(iteration), "")
    
    ### 2. Parse and print results in CSV and TSV format
    print_result(outdir, target, target_list, timelimit,  iteration, tools)



if __name__ == "__main__":
    main()
