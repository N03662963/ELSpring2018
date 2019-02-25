#!/bin/bash
#Sadia Khan 2/19/2019
clear
#user inputs 2 Integers
echo "Input First Integer:"
read x
echo "Input Second Integer:"
read y
#decide what to do with them
echo "Select from 1 to 4:
1. Addition
2. Subtraction
3. Multiplication
4. Division"

read sel

#go through case statements
case $sel in
	#1)Addition
	1)answer=$(($x + $y));;
	#2)Subtraction
	2)answer=$(($x - $y));;
	#3)Multiplication
	3)answer=$(($x * $y));;
	#4)Division (use built in calculator(bc) to scale it to three dec)
	4)answer=`echo "scale=3; $x / $y" | bc`;;
esac

#Print the final Result
echo "The Result = $answer"




