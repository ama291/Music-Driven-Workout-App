#!/bin/sh

for file in Tests/*; do
  ext=${file##*.}
  base=$(basename ${file})
  module=${base%.*}
  if [ "${ext}" = "py" ] && [ "${module}" != "__init__" ]; then
    echo ${module}
    python -m Tests.${module}
  fi
done
