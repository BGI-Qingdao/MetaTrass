**MetaTrass © BGI-Qingdao**
---

Description:
---
**MetaTrass** is abbrivation to **Meta**genomics **T**axonomic **R**eads For **A**ssembly **S**ingle **S**pecies. MetaTrass is based on high-quality referencess with taxonomic tree and long-range information encoded within co-barcoded short-read sequences. The comprehensive use of co-barcoding information and references in our approach can reduce the false negative effects of genome taxonomy by using co-barcoding information while reduce the false positive effects of co-barcoding information by using references.

Publication:
---

+ biorxiv: [MetaTrass]().

Change Log:
---

* v1.1.0 (2021-07-09) - Fixed a few bugs
* v1.0.0 (2021-04-13) - Initial release

Dependencies:
---

+ Python: Version >3.0.0

+ C++ libraries: C++11 standard library

+ Third-party software:  [stLFR_barcode_split](https://github.com/BGI-Qingdao/stLFR_barcode_split.git),
[Kraken2](http://ccb.jhu.edu/software/kraken2/), 
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

2. You can either add MetaTrass's 3rd party dependencies to your system path or specify full path to alias into the folder `MetaTrass/tools/` which can be found MetaTrass easily. 

Preparing before complementation:
---
1. **The input files** for MetaTrass include a folder that holds the sequence file of all query genomes.
     * stLFR data all are welcome!
     * if you have demand of others co-barcode data analyses demand, please contact us.

2. **The reference database** for kraken2 include a folder that holds the database. 
   Databases are pre-built, including the required hash.k2d, opts.k2d, and taxo.k2d files.
     * for human gut: 
        we recommend the UHGG taxonomy database which can be download from [MGnify Genomes](http://ftp.ebi.ac.uk/pub/databases/metagenomics/mgnify_genomes/human-gut/v1.0/uhgg_kraken2-db/).
     * for Zymo 10 Mock:
        You can download the reference database from [Mock Community]()

     * or for customized microbiome grouping:
        Please check the official species taxonomic ID to add into the NCBI.

     * For a realiable construction of the species tree, the reference genomes for MetaTrass should be non-redundant genome of all single-speices. :warning:

3. **The reference genome** for refining the contigs should be kept with the reference database.
     * Split library.fna to each single species fasta file
      You can use the script (MetaTrass/script/fa_split_by_taxid.py) to covert the library.fna to single species fasta file. 
      
     * If you already have the single-species, please ensure the filename format with taxid_genomic.fa, such as 1104_genomic.fa.

4. **The reference genome** length information :warning: .
      * Get each of single species genome size as the configure file with two column:
        table example:
	
		|taxid	 | genome size(bp)|
		| :----- | ----: |
		|1000|2176737|
		|1001|6092914|
      * Please note that the genome size table file without any headline. :warning: :warning: :warning:

How to run:
---
1. Usage:
 	* First Step: //Get CleanData 
	```	
	MetaTrass GC	--barcodeSplit  
			--filtering 
	```
	* Second Step: //Taxonomic Reads and Co-Barcoding Enrich Reads 
	```	
	MetaTrass TR 	--threads  
			--mem  
			--ref_db   
			--min_depth   
			--max_depth    
			--input   
			--output  
	```

 	* Third Step: //Single-species Assembly and Contigs refining  
	```
	MetaTrass SA 	--threads  
			--mem  
			--ref_fa  
			--min_depth  
			--max_depth  
			--input  
			--output  
	```
	
2. Examples:
    * Please refer to the  MetaTrass/bin/test.sh


Output files:
---
1. Examples of output folder structure

    * step1_cleandata
    * step2_taxonomy
    * step3_assembly
    * step4_assessment
    * step5_binfilter


Contributing:
---
* Author: [Yanwei Qi](https://github.com/QYanwei), [Lidong Guo](https://github.com/cchd0001).

License:
---
* GNU General Public License v3.0 [![pypi licence](https://img.shields.io/pypi/l/MetaCHIP.svg)](https://opensource.org/licenses/gpl-3.0.html)
