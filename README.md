**MetaTrass © BGI-Qingdao**
---

Description:
---
**MetaTrass** is abbreviation to **Meta**genomics **T**axonomic **R**eads For **A**ssembly **S**ingle **S**pecies. MetaTrass is based on high-quality referencess with taxonomic tree and long-range information encoded within co-barcoded short-read sequences. The comprehensive use of co-barcoding information and references in our approach can reduce the false negative effects of genome taxonomy by using co-barcoding information while reduce the false positive effects of co-barcoding information by using references.

Publication:
---

+ biorxiv: [MetaTrass]().

Change Log:
---
* v1.2.0 (2021-08-03) - Finished a version test!
* v1.1.0 (2021-07-09) - Fixed a few bugs
* v1.0.0 (2021-04-13) - Initial release

Dependencies:
---

+ Python: Version >3.0.0

+ C++ libraries: C++11 standard library

+ Third-party software:  [stLFR_barcode_split](https://github.com/BGI-Qingdao/stLFR_barcode_split.git),
[Kraken2](https://github.com/DerrickWood/kraken2), 
[Seqtk](https://github.com/lh3/seqtk.git), 
[stlfr2supernova](https://github.com/BGI-Qingdao/stlfr2supernova_pipeline) and 
[Quast](http://quast.sourceforge.net/quast.html)

How to install:
---
1. MetaTrass can be installed via git channel:

        # First-time installation
        git clone https://github.com/BGI-Qingdao/MetaTrass.git

        # for upgrade
        git add *

2. You can either add MetaTrass's 3rd party dependencies to your system path or put specify full path to alias into the folder `MetaTrass/tools/` which can be found MetaTrass easily. 

Preparing before complementation:
---
1. **The input files** for MetaTrass include a folder that holds the sequence file of all query genomes.
     * stLFR data all are welcome!  
     * If you have the demand of others co-barcode data analyses, please contact us.

2. **The reference database** for kraken2 include a folder that holds the database. 
   Databases are pre-built, including the required hash.k2d, opts.k2d, and taxo.k2d files.
     * For **Human Gut**:  
       We recommend the UHGG taxonomy database which can be download from [MGnify Genomes](http://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/v1.0/uhgg_kraken2-db/).  
       **uhgg_kraken2-db/**  
				├── [472K]  database100mers.kmer_distrib  
				├── [441K]  database150mers.kmer_distrib  
				├── [421K]  database200mers.kmer_distrib  
				├── [403K]  database250mers.kmer_distrib  
				├── [540K]  database50mers.kmer_distrib  
				├── [4.0K]  library    
				│   ├── [ 11G]  **library.fna**  
				│   └── [ 31M]  prelim_map.txt  
				├── [ 16G]	**hash.k2d**  
				├── [  48]	**opts.k2d**  
				├── [473K]	**taxo.k2d**  
				└── [4.0K]  taxonomy  
				    ├── [310K]  names.dmp  
				    ├── [127K]  nodes.dmp  
				    └── [ 31M]  prelim_map.txt  

     * For [**Zymo Community Standards 10 Mock**](https://github.com/LomanLab/mockcommunity):  
       You can download the reference database from [Mock Community](https://lomanlab.github.io/mockcommunity/mc_databases.html)

     * Or for **Customized Microbiome** grouping:  
       Please check the NCBI official species taxonomic ID to add into the NCBI taxonomy.  
       To build a realiable construction of the species tree, please remind that the reference genomes for MetaTrass should be non-redundant genome of all single-speices. :warning:

3. **The reference genome** for refining the contigs should be kept with the reference database.
     * Split library.fna which can find in uhgg_kraken2-db/library/ (see above) to each single species fasta file  
      You can use the script (MetaTrass/script/fa_split_by_taxid.py) to covert the library.fna to single species fasta file. 
      
     * If you already have the single-species, please ensure the filename format with taxid_genomic.fa, such as 1104_genomic.fa.

4. **The reference genome size** information. :warning:
      * Get each of single species genome size as the configure file with two column:  
        table example:  
	
		|taxid	 | genome size(bp)|
		| :----- | ----: |
		|1000|2176737|
		|1001|6092914|
		|1002|3864718|
		|1006|2741290|
		|1007|3003526|
		|1008|1739566|
		|1009|1809170|
		|1010|4528241|
		|1011|2149385|
		|1013|2260187|

      * Please note that the genome size table file without any header line. :warning: :warning: :warning:

How to run:
---
1. Usage:
 	* Getting CleanData 
	```	
	> python Trass.py GC -h
	usage: Trass.py GC [-h] -rawfq1 RAWFQ1 -rawfq2 RAWFQ2 [-thread THREAD] -outdir OUTDIR [-runnow RUNNOW]

	Get stLFR Cleandata

	optional arguments:
	  -h, --help      show this help message and exit
	  -rawfq1 RAWFQ1  Paired-end data: raw 1 fastq.gz
	  -rawfq2 RAWFQ2  Paired-end data: raw 2 fastq.gz
	  -thread THREAD  the number of threads
	  -outdir OUTDIR  Output folder
	  -runnow RUNNOW  Run this script immediately

	```
	
	* **T**axonomic Reads **A**nd Co-**B**arcoding Reads **Refining**  (TABrefiner)
	```	
	> python Trass.py TB -h
	usage: Trass.py TB [-h] -cleanfq1 CLEANFQ1 -cleanfq2 CLEANFQ2 [-thread THREAD] [-parallel PARALLEL] -sample SAMPLE -ref_db REF_DB -genome_size GENOME_SIZE [-max_depth 		MAX_DEPTH] [-min_depth MIN_DEPTH] [-pe_length PE_LENGTH] -outdir OUTDIR [-runnow RUNNOW]

	Taxnomic and Barcoding

	optional arguments:
	  -h, --help            show this help message and exit
	  -cleanfq1 CLEANFQ1    Paired-end data: cleanfq1 fastq.gz
	  -cleanfq2 CLEANFQ2    Paired-end data: cleanfq2 fastq.gz
	  -thread THREAD        Kraken parameter
	  -parallel PARALLEL    The number of parallel species
	  -sample SAMPLE        Output FileName Prefix
	  -ref_db REF_DB        Taxonomy references database
	  -genome_size GENOME_SIZE
				Reference genome size table file
	  -max_depth MAX_DEPTH  Species Maximum-Depth Required Assembly
	  -min_depth MIN_DEPTH  Species Minimum-Depth Required Assembly
	  -pe_length PE_LENGTH  PE read length of sequencing data
	  -outdir OUTDIR        Output folder
	  -runnow RUNNOW        Run this script immediately
  
	```

 	* Single-species **Assembly** and Contigs **Purifying**  
	```
	> python Trass.py AP -h
	usage: Trass.py AP [-h] [-maprate MAPRATE] [-memory MEMORY] [-maxreads MAXREADS] [-pairdepth PAIRDEPTH] [-PCT PCT] [-IDY IDY] -ref_fa REF_FA [-thread THREAD]
	[-parallel PARALLEL] [-max_depth MAX_DEPTH] [-min_depth MIN_DEPTH] -outdir OUTDIR [-runnow RUNNOW]

	Assembly and Purifying

	optional arguments:
	  -h, --help            show this help message and exit
	  -maprate MAPRATE      mapping ratio (default=8)
	  -memory MEMORY        number of memory use(GB,default = 150)
	  -maxreads MAXREADS    maximumreads for supernova(default = 2140000000)
	  -pairdepth PAIRDEPTH  filter less X pair barcode reads(default = 2)
	  -PCT PCT              Threshold of contig lnegth(0-1)
	  -IDY IDY              Threshold of IDY (80 - 100)
	  -ref_fa REF_FA        Taxonomic reference genome fasta folder
	  -thread THREAD        The number of assembly thread of each species
	  -parallel PARALLEL    The number of parallel assembly of single species
	  -max_depth MAX_DEPTH  Species Maximum-depth required assembly
	  -min_depth MIN_DEPTH  Species Minimum-depth required assembly
	  -outdir OUTDIR        Output folder
	  -runnow RUNNOW        Run this script immediately

	```
	
2. Examples:
    * Please refer to the  MetaTrass/bin/test.sh


Output files:
---
1. Examples of output folder structure
.
├── all_command_shell
│   ├── run.log
│   ├── stp2.1.kraken2taxon.sh
│   ├── stp2.2.TXACBrefiner.sh
│   ├── stp2.3.ReadID2Fastq.sh
│   ├── stp3.1.MetaAssembly.sh
│   └── stp3.2.ContigPurify.sh
├── dir1_cleandata
│   ├── barcode_freq.txt 
│   ├── lane.lst 
│   ├── split_reads.1.fq.gz.clean.gz 
│   ├── split_reads.2.fq.gz.clean.gz 
│   ├── split_read_stat.log 
│   └── stat.txt 
├── dir2_taxonomy
│   ├── ID2FQ
│   ├── kraken
│   └── SSRlist
└── dir3_assembly
    ├── purify
    ├── quast
    └── supernova

10 directories, 12 files

Contributing:
---
* Author: [Yanwei Qi](https://github.com/QYanwei), [Lidong Guo](https://github.com/cchd0001).

License:
---
* GNU General Public License v3.0 [![pypi licence](https://img.shields.io/pypi/l/MetaCHIP.svg)](https://opensource.org/licenses/gpl-3.0.html)
