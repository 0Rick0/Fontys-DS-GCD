#!/bin/sh
function run_many(){
    number=$1
    echo "Running ${number} workers"
    shift
    for i in `seq $number`; do
	    $@&
    done
    wait -n
}

echo "How many processes to run with?"
read count

python3 MapReduce_code.py &
reduce_pid=$!

echo "Press enter when ready appears"
read

time run_many ${count} python3 mincemeat.py -p changeme localhost
wait ${reduce_pid} # wait for the job to finish