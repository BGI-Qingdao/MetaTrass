python /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/bin/main.py \
-sample CL100164780_L01 \
-fq1 /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/rawfq/CL100164780_L01_read_1.fq.gz \
-fq2 /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/rawfq/CL100164780_L01_read_2.fq.gz \
-outdir /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/test/ \
-label stlfr \
-min_depth 10 \
-max_depth 300 \
-threads  20 \
-strategy both \
-idba_ud yes \
-supernova yes \
-quast no \
-checkm no \
-IDY 90 \
-PCT 0.5 \
-kraken_db /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/database/kraken/uhgg_kraken2-db \
-kraken_fa /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/database/kraken/uhgg_kraken2-fa \
-genome_sz /zfsqd1/ST_OCEAN/USRS/qiyanwei/pipeline/MetaTrass/source/all_single_species_genome_size.uhgg.txt
