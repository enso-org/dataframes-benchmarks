#!/bin/bash
set -xe

rm enso_times.csv || true
rm python_times.csv || true

for i in {1..20}
do
    echo "Run $i"

    (cd python/ && python baseline.py 2>/dev/null | paste -s -d, /dev/stdin >> ../python_times.csv)

    enso run . 2>/dev/null | sed -e 's/,/./g' | paste -s -d, /dev/stdin >> enso_times.csv
done
