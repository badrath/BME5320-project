#!/bin/bash
# SCRIPT:  primefactors.sh
# USAGE :  primefactors.sh <Positive Integer>
# PURPOSE: Produces prime factors of a given number.
#
###############################################################################
#                           Arguments Checking                                #
###############################################################################
if [ $# -ne 1 ]
then
echo "Usage: scriptname <Positive Integer>"
exit 1
fi
expr $1 + 1  &>/dev/null
if [ $? -ne 0 ]
then
echo "Sorry, You supplied non numerical value"
exit 1
fi
[ $1 -lt 2 ] && echo "Values < 2 are not prime numbers" && exit 1
num=$1
###############################################################################
#                              Functions                                      #
###############################################################################
# To know how to find prime number check bellow link:
# Shell script to find prime number
# Bellow function finds supplied argument is a prime or not.
primenumber()
{
primenum=$1
for ((counter2=2;$((counter2*counter2))<=$primenum;counter2++))
do
if [ $((primenum%counter2)) -eq 0 ]
then
return 1
fi
done
return 0
}
primefind()
{
# It's good to check that the number it self is a prime or not before going to
# find prime factors of a number. Comment out bellow line and supply a prime
# number or semi-prime, you will find the difference.
# Ex: primefactors.sh 2121979
primenumber $1 && echo "$1" && exit 0
for ((counter1=$2;counter1<=$1;counter1++))
do
primenumber $counter1 && factorcheck $1 $counter1 &&  break
done
}
factorcheck()
{
prime=$2
newnum=$1
remainder=$((newnum%prime))
if [ $remainder -eq 0 ]
then
printf "%d " $prime
newnum=$((newnum/prime))
primefind $newnum 2
return
else
let prime++
primefind $newnum $prime
fi
}
###############################################################################
#                                   Main                                      #
###############################################################################
echo -n #"Prime Factors of $1: "
primefind $num 2
printf "\b \n"                   # \b is used for removing last x.