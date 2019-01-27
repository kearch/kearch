#!/bin/bash

set -eux
shopt -s expand_aliases

cd $(dirname $0)/..
REPO_DIR=$(pwd)

LOG_DIR=~/logs/kearch
date_str=$(date +%Y%m%d%H%M%S)
host=${1:-'163.43.108.218'}
port=${2:-2222}

alias kgponamel="kubectl get pod -o go-template --template '{{(index .items 0).metadata.name}}' -l"
mkdir -p $LOG_DIR


kubectl delete pod -n kearch --all

python3 -u benchmark/benchmarker.py -H $host -p $port 2>&1 | tee $LOG_DIR/siege-all_$date_str.log
cp $LOG_DIR/siege-all_$date_str.log $LOG_DIR/siege-all_latest.log

for engine in "sp" "me"; do
  kubectl exec $(kgponamel engine=$engine,app=db) -- cat /var/log/mysql/slow.log > $LOG_DIR/$engine-db-slow_$date_str.log
  /usr/local/bin/pt-query-digest --limit 10 $LOG_DIR/$engine-db-slow_$date_str.log > $LOG_DIR/pt-$engine-db_$date_str.log
  cp $LOG_DIR/$engine-db-slow_$date_str.log $LOG_DIR/$engine-db-slow_latest.log
  cp $LOG_DIR/pt-$engine-db_$date_str.log $LOG_DIR/pt-$engine-db_latest.log
done
