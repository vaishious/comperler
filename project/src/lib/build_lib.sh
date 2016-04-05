#!/usr/bin/bash

CWDIR="/home/rbavishi/Courses/CS335/comperler/mips-x86.linux-xgcc"
export PATH+=":$CWDIR"

../../../mips-x86.linux-xgcc/mips-gcc -S arraylib.c
../../../mips-x86.linux-xgcc/mips-gcc -S hashlib.c
../../../mips-x86.linux-xgcc/mips-gcc -S iolib.c
../../../mips-x86.linux-xgcc/mips-gcc -S libstd.c
../../../mips-x86.linux-xgcc/mips-gcc -S libstring.c
