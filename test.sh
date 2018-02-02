#!/bin/sh 

for file in Tests/*; do
  ext=${file##*.}
  base=$(basename ${file})
  module=${base%.*}
  if [ "${ext}" = "py" ]; then
    python -m Tests.${module}
  fi
done
