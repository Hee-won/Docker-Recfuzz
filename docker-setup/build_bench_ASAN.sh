#!/bin/bash

. $(dirname $0)/build_bench_common.sh

# arg1 : Target project
# arg2~: Fuzzing targets
function build_with_ASAN_swftophp() {
    CC="/usr/bin/gcc"
    CXX="/usr/bin/g++"
        
    for TARG in "${@:2}"; do
        cd /benchmark

        str_array=($TARG)
        BIN_NAME=${str_array[0]}

        build_target $1 $CC $CXX "-fsanitize=address -fno-omit-frame-pointer"
        for BUG_NAME in "${str_array[@]:1}"; do
            copy_build_result $1 $BIN_NAME $BUG_NAME "ASAN"
        done
    done
    rm -rf RUNDIR-$1 || exit 1
}


function build_with_ASAN() {    
    for TARG in "${@:2}"; do
        cd /benchmark

        str_array=($TARG)
        BIN_NAME=${str_array[0]}

        build_target $1 "clang" "clang++" "-fsanitize=address"
        for BUG_NAME in "${str_array[@]:1}"; do
            copy_build_result $1 $BIN_NAME $BUG_NAME "ASAN"
        done
    done
    rm -rf RUNDIR-$1 || exit 1
}


# Build with ASAN only
mkdir -p /benchmark/bin/ASAN
build_with_ASAN_swftophp "libming-4.7" \
    "swftophp-4.7 2016-9827 2016-9829 2016-9831 2017-9988 2017-11728 2017-11729 2017-7578"&
wait

build_with_ASAN_swftophp "libming-4.8" \
    "swftophp-4.8 2018-7868 2018-8807 2018-8962 2018-11095 2018-11225 2018-11226 2020-6628 2018-20427 2019-12982 2019-9114" &

wait

build_with_ASAN "binutils-2.26" \
    "cxxfilt 2016-4487 2016-4489 2016-4490 2016-4491 2016-4492 2016-6131" &

wait

build_with_ASAN "binutils-2.28" \
    "objdump 2017-8392 2017-8396 2017-8397 2017-8398"