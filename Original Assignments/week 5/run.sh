#!/bin/bash
number=$1
shift
for i in `seq $number`; do
	$@&
done
wait -n
