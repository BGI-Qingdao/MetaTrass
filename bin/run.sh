rawfq1=$1
rawfq2=$2
sample=$3
outdir=$4
mkdir -p $outdir 

output=$outdir/$sample
mkdir -p $output

python="/path/to/python3"
Trass="/path/to/MetaTrass/Trass.py"
ref_db="/path/to/uhgg_kraken2-db/"
ref_fa="/path/to/uhgg_kraken2-fa/"
ref_gz="/path/to//MetaTrass/config/all_single_species_genome_size.uhgg.txt"
echo $python $Trass GC -rawfq1 $rawfq1 -rawfq2 $rawfq2 -outdir $output -runnow yes
echo $python $Trass TB -cleanfq1 $output/dir1_cleandata/split_reads.1.fq.gz.clean.gz -cleanfq2 $output/dir1_cleandata/split_reads.2.fq.gz.clean.gz -thread 30 -sample $sample -ref_db $ref_db -genome_size $ref_gz -outdir $output -runnow yes
echo $python $Trass AP -outdir $output -ref_fa $ref_fa -thread 10 -parallel 10 -runnow yes

#echo rm -f $output/dir1_cleandata/split_reads.1.fq.gz $output/dir1_cleandata/split_reads.2.fq.gz
#echo rm -f $output/dir2_taxonomy/kraken/$sample.C
#echo rm -f $output/dir2_taxonomy/ID2FQ/*fq.gz

