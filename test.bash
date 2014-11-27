#!/bin/bash
mkdir keyword;
DIR=en
TOOL="python html_tool.py"
for file in $DIR/*.html
do
	if test -f $file
	then
		$TOOL e $file
		mv "$file.offset" keyword/
	else
		print "NOT FOUND"
	fi
done

for file in $DIR/*.htm
do
	if test -f $file
	then
		echo $TOOL
		$TOOL e $file
		mv "$file.offset" keyword/
	else
		print "NOT FOUND"
	fi
done

for file in $DIR/*.js
do
	if test -f $file
	then
		$TOOL e $file
		mv "$file.offset" keyword/
	else
		print "NOT FOUND"
	fi
done
