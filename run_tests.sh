#!/usr/bin/env bash

# Colors
N="\033[0m"       # Unset colors
R="\033[0;31m"    # red
G="\033[0;32m"    # green

function run_test_case() {
    # if arg1 is defined and file R$1.in exists
    if [ -z $1 ] && [ ! -f "R$1.in" ]; then
        echo -e "${R}Missing test file R$1${N}"
        return 2
    fi

    echo -n -e "Test $1"
    python ../src/CF.py < R$1.in > R$1.my.out
    diff -q R$1.out R$1.my.out > /dev/null
    if [ $? -eq 0 ]; then
      echo -e "${G} passed! ${N}"
    elif [ $? -eq 1 ]; then
      echo -e "$R failed! $N"
    fi
}

cd integration_tests
echo "Starting tests..."
run_test_case 0
run_test_case 1
run_test_case 2
echo "All tests completed!"
cd ..
