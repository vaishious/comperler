#!/usr/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";

$SCRIPT_DIR/irgen $1;

IR_FILE=`echo $1 | cut -d'.' -f 1`".ir";
IR_FILE=`basename $IR_FILE`;
SYMTAB_FILE=`echo $1 | cut -d'.' -f 1`".sym";
SYMTAB_FILE=`basename $SYMTAB_FILE`;
echo "### IR ###";
cat $IR_FILE
echo "";
echo "### SYMBOL TABLES ###";
echo "";
cat $SYMTAB_FILE;

