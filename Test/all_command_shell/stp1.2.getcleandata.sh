cp /Users/GitHub/MetaTrass/config//lane.lst /Users/GitHub/MetaTrass/Test//dir1_cleandata//lane.lst 
cd /Users/GitHub/MetaTrass/Test//dir1_cleandata/ 
/Users/GitHub/MetaTrass/tools//SOAPfilter -t 20 -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -y -p -M 2 -f -1 -Q 10 lane.lst stat.txt
