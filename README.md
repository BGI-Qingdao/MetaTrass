# MetaTrass

## Description
**MetaTrass:** **T**axonomic **R**eads **F**or **A**ssembly **S**ingle **S**pecies to **Meta**genomics

We developed an assembling pipeline named MetaTrass with using both high quality references in public databases and long-range information encoded within co-barcoded short-read sequences. With great potential in genome assembly of co-barcoded library, many different co-barcoded libraries have been reported recently, but the single tube long fragment read library have been used in developing our tool. The comprehensive use of co-barcoding information and references in our approach can reduce the false negative effects of genome taxonomy by using co-barcoding information while reduce the false positive effects of co-barcoding information by using references.

## Usage:

usage: trass.py [-h] 
               -sample SAMPLE \
               -fq1 FQ1 \
               -fq2 FQ2 \
               -outdir OUTDIR \
               -label LABEL \
               -min_depth MIN_DEPTH \
               -max_depth MAX_DEPTH \
               -kraken_db KRAKEN_DB \
               -kraken_fa KRAKEN_FA \
               -genome_sz GENOME_SZ \
               -threads THREADS \
               -strategy STRATEGY \
               -idba_ud IDBA_UD \
               -supernova SUPERNOVA \
               -quast QUAST \
               -checkm CHECKM \
               -IDY IDY \
               -PCT PCT
## Result:
### Rank-Completeness Results
![image](https://user-images.githubusercontent.com/13197453/114501922-7c864d00-9c5d-11eb-8025-4d1b6a2add01.png)
### Scaffold N50
![image](https://user-images.githubusercontent.com/13197453/114502014-9f186600-9c5d-11eb-8372-9cf1fc624fc6.png)

## Contributing
This project exists thanks to all the people who contribute. 

https://github.com/QYanwei \
https://github.com/cchd0001 \
https://github.com/xiaoqiang435 \

## License
GNU General Public License v3.0 © BGI-Qingdao
