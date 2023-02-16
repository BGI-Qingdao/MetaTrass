rawfq1=$1
rawfq2=$2
sample=$3
outdir=$4
#mkdir -p $outdir 

output=$outdir/
mkdir -p $output

python="/path-to/conda3/bin/python"
Trass="/path-to/MetaTrass/Trass.py"
ref_db="/path-to/MetaTrass_Resource/database/uhgg_kraken2-db/"
ref_fa="/path-to/MetaTrass_Resource/database/uhgg_kraken2-fa/"
ref_gz="/path-to/MetaTrass_Resource/database/uhgg_kraken2-fa/ref_genome_size.txt"
echo $python $Trass GC -rawfq1 $rawfq1 -rawfq2 $rawfq2 -outdir $output -runnow yes
echo $python $Trass TB -cleanfq1 $output/dir1_cleandata/split_reads.1.fq.gz.clean.gz -cleanfq2 $output/dir1_cleandata/split_reads.2.fq.gz.clean.gz -thread 5 -sample $sample -ref_db $ref_db -genome_size $ref_gz -outdir $output -runnow yes -min_depth 5
echo $python $Trass AP -outdir $output -ref_fa $ref_fa -thread 5 -parallel 1 -runnow yes -min_depth


