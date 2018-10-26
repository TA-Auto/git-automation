#!/bin/bash

for d in monorepo-*; do 
  cp 2.*.py "${d}/Assignment4_Shell"
  if [ -e Makefile ]
  then
    make -C  "${d}/Assignment4_Shell"
  else
    gcc -std=c99 -o "${d}/Assignment4_Shell/shell" "${d}/Assignment4_Shell/shell.c"
  fi

done
