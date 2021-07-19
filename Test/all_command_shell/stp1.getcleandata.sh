cp /Users/yanweiqi/GitHub/MetaTrass/config//lane.lst ./Test/dir1_cleandata//lane.lst 
cd ./Test/dir1_cleandata/ 
/Users/yanweiqi/GitHub/MetaTrass/tools//SOAPfilter -t 20 -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10 lane.lst stat.txt
cp /Users/yanweiqi/GitHub/MetaTrass/config//lane.lst /Users/yanweiqi/GitHub/MetaTrass/Test/dir1_cleandata//lane.lst 
cd /Users/yanweiqi/GitHub/MetaTrass/Test/dir1_cleandata/ 
/Users/yanweiqi/GitHub/MetaTrass/tools//SOAPfilter -t 20 -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10 lane.lst stat.txt
