#!/usr/bin/bash
buku --nostdin -p -f4 | awk -F '\t' 'BEGIN {OFS="\t"}; 
{print $1, "\033[32m"$4"\033[0m", "\033[33m"$2"\033[0m", "\033[36m"$3"\033[0m" }'



