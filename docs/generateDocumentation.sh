#!/bin/bash
cd docs
cat listForDocumentation.txt | while read line
do
   #echo $line
   python -m pydoc ../src/${line}.py >> "build/${line}_doc.txt"
done