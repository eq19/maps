# formatting script for the prime number files
# currently just removes the commas

# list of only the text files
pfiles=$(ls *.txt)

#remove commas and rename files by lowest number
for p in $pfiles
do
  touch tempfile
  sed -e 's/,/ /g' $p > tempfile
  read lower_limit _ < tempfile
  rm $p
  mv tempfile ${lower_limit}.txt
done
