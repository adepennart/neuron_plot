#!/bin/bash
# Basic if statement
cat forlooped_2.txt| while read line;
 do num=$(echo $line|cut -d ' ' -f 1);
species=$(echo $line| cut -d ' ' -f 2)
 angle=$(echo $line | cut -d ' ' -f 3,4,5);
NO_L=$(echo $line|cut -d ' ' -f 6);
NO_R=$(echo $line|cut -d ' ' -f 7);
NO_COL=$(echo $line|cut -d ' ' -f 8,9);
#echo $NO_L $NO_R $NO_COL;
if [ $NO_R = 'NO_R' ]
then 
	python3 plot_pymaid.py -i $num -j input/catmaid-skeletons-2022-5-25_$species.json -p \
	$angle -s -V EB PB FB $NO_L $NO_R -C 0,1,0,0.1 0,1,0,0.1 0,1,0,0.05 $NO_COL \
	-o ${species}_fig
else
	python3 plot_pymaid.py -i $num -j input/catmaid-skeletons-2022-5-25_$species.json -p \
 	$angle -s -V EB PB FB $NO_L -C 0,1,0,0.1 0,1,0,0.1 0,1,0,0.05 $NO_R \
 	-o ${species}_fig;
fi;
done


