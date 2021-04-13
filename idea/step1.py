#!/usr/bin/env python
#-*-coding:utf-8-*-

import yaml
import sys
import os
import shutil
import re

def config_check_and_get_info(para_data):
    work_dir=para_data['work_dir']
    #sample=para_data['sample'].strip().split(';')
    #kraken=para_data['kraken']
    #kraken_result=para_data['kraken_result']
    read1=para_data['raw_data']['read1']
    read2=para_data['raw_data']['read2']
    strategy=para_data['strategy']
    python_path=para_data['python_path']
    script_path=para_data['script_path']
    seqkit_path=para_data['seqkit_path']
    print 'all result output to '+work_dir

    if (work_dir=='' or re.match(r'\s+',work_dir)) or (strategy=='' or re.match(r'\s+',strategy)) or (seqkit_path=='' or re.match(r'\s+',seqkit_path)) or (python_path=='' or re.match(r'\s+',python_path)) or (script_path=='' or re.match(r'\s+',script_path)) or (read1=='' or re.match(r'\s+',read1)) or (read2=='' or re.match(r'\s+',read2)):
        print 'at least one required parameters not be given, please check config file'
        sys.exit()
    
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.mkdir(work_dir)

    global sample_list
    sample_list=[]
    try:
        para_data['abundance']['select']
    except:
        sample=para_data['sample'].strip().split(';')
        if ('all' in sample or 'default' in sample) and len(sample)>1:
            print 'sample list error, all could not set with other sample'
            sys.exit()
        elif 'all' in sample and len(sample)==1:
            try:
                inputs=open(para_data['kraken_result'])
            except:
                print "when sample is set 'all', kraken_result must be set at same time"
                sys.exit()
            else:
                for i in inputs:
                    sample_list.append(i.split('\t')[2])
            sample_list=list(set(sample_list))
            with open(work_dir+'/sample_list','w') as output:
                for i in sample_list:
                    print >>output,i
        else:
            sample_list=sample
            with open(work_dir+'/sample_list','w') as output:
                for i in sample:
                    print >>output,i
    else:
        try:
            para_data['abundance']['taxonomy_info']
        except:
            print 'no taxonomy info is set, please provide this.'
            sys.exit()
        else:
            global select
            select=para_data['abundance']['select']
            print 'the species is choose the '+select+' species from abundance result'
    if strategy=='all':
        strategy=['all_read','all_barcode','unique_barcode']
    elif len(strategy.split(';'))==2 or len(strategy.split(';'))==3:
        strategy=strategy.split(';')
    elif len(strategy)==1:
        strategy=[strategy]
    else:
        print 'wrong strategy set, please change it in config file'
        sys.exit()
    process=[]
    try:
        para_data['stLFRQC']
    except:
        pass
    else:
        process.append('stlfrqc')
    try:
        para_data['denovo']
    except:
        pass
    else:
        try:
            para_data['denovo']['supernova']
        except:
            pass
        else:
            process.append('supernova')
        try:
            para_data['denovo']['idba']
        except:
            pass
        else:
            process.append('idba') 
        try:
            para_data['denovo']['quast']
        except:
            pass
        else:
            process.append('quast')
        try:
            para_data['denovo']['filt']
        except:
            pass
        else:
            process.append('filt')
    
    global final_process
    final_process={}
    for ii in sample_list:
        ii=str(ii)
        final_process[ii]={}
        for ll in strategy:
            final_process[ii][ll]=[]
            for kk in process:
                final_process[ii][ll].append(kk)

def mk_dir(final_process):
    work_dir=para_data['work_dir']
    os.mkdir(os.path.join(work_dir,'result'))
    os.mkdir(os.path.join(work_dir,'result','step1'))
    #os.mkdir(os.path.join(work_dir,'kraken'))
    os.mkdir(os.path.join(work_dir,'shell'))
    os.mkdir(os.path.join(work_dir,'shell','step1'))
    #os.system('cp '+para_data['script_path']+'/remove_no_need_dir.py '+os.path.join(work_dir,'shell'))
    #for sample in final_process:
    #    os.mkdir(os.path.join(work_dir,'shell',str(sample)))
    #    os.mkdir(os.path.join(work_dir,str(sample)))
    #    for strategy in final_process[sample]:
    #        os.mkdir(os.path.join(work_dir,str(sample),strategy))
    #        os.mkdir(os.path.join(work_dir,'shell',str(sample),strategy))
    #        for process in final_process[sample][strategy]:
    #            os.mkdir(os.path.join(work_dir,str(sample),strategy,process))
    
def run_kraken(para_data):
    shell_path=os.path.join(para_data['work_dir'],'shell','step1','run_kraken.sh') 
    result_path=os.path.join(para_data['work_dir'],'result','step1')
    with open(shell_path,'w') as SHELL:
        print  >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
        print >>SHELL,para_data['kraken']['path']+' --threads '+str(para_data['kraken']['thread'])+' --gzip-compressed --paired --db '+para_data['kraken']['taxonomy_path']+' --output '+result_path+'/kraken_result.C --report '+result_path+'/kraken_result.report '+para_data['raw_data']['read1']+' '+para_data['raw_data']['read2']+' &&'
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
    para_data['kraken_result']=result_path+'/kraken_result.C'
    #return para_data

def classify_kraken(final_process):
    kraken_result=para_data['kraken_result']
    #filename=os.path.basename(kraken_result)
    final_filename='final_kraken_result.C'
    read1=para_data['raw_data']['read1']
    shell_path=os.path.join(para_data['work_dir'],'shell','step1','classify_kraken_result.sh')
    result_path=os.path.join(para_data['work_dir'],'result','step1')
    with open(shell_path,'w') as SHELL:
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
        print >>SHELL,'ln -s '+kraken_result+' '+result_path+'/'+final_filename+' &&'
        print >>SHELL,"awk -F '\\t' '{if($3!=0)print $0}' "+os.path.join(result_path,final_filename)+" > "+os.path.join(result_path,final_filename+'_classify.list')+" &&"
        print >>SHELL,"awk -F '\\t' '{if($3==0)print $0}' "+os.path.join(result_path,final_filename)+" > "+os.path.join(result_path,final_filename+'_unclassify.list')+" &&"
        print >>SHELL,"awk -F '\\t' '{print $2}' "+os.path.join(result_path,final_filename)+' > '+os.path.join(result_path,"all_seq_id.list")+' &&'
        #print >>SHELL,"less -S "+read1+"| awk -F '' '{if($1==\"@\" && $2==\"C\" && $3==\"L\")print $0}' - | awk -F ' ' '{print $1}' - >"+os.path.join(result_path,"all_seq_id.list")+' &&'
        #print >>SHELL,"awk -F '#' '{print $2}' "+result_path+"/all_seq_id.list |awk -F '/' '{print $1}' - > "result_path+"/all_seq_barcode.list"+' &&'
        print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/get_all_sample_uniq_barcode_reads.py '+os.path.join(result_path,final_filename+'_classify.list')+' '+result_path+' &&'
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def abundance(para_data):
    kraken_result=para_data['work_dir']+'/shell/step1/final_kraken_result.C_classify.list'
    ref_dir=para_data['abundance']['ref_dir']
    shell_path=os.path.join(para_data['work_dir'],'shell','step1','kraken_result_abundance.sh')  
    result_path=os.path.join(para_data['work_dir'],'result','step1')
    with open(shell_path,'w') as SHELL:
       print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
       print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/get_reads_abundance.py '+kraken_result+' '+result_path+' '+ref_dir
       if select:
           print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/get_species_from_abundance.py '+result_path+'/all_taxid_abundance.sort.matrix '+para_data['work_dir']+' '+select
       print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
        
def get_reads(final_process):
    kraken_file=os.path.join(para_data['work_dir'],'result','step1','final_kraken_result.C_classify.list')
    sample_file=para_data['work_dir']+'/sample_list'
    for sp in final_process:
        #sp=str(sp)
        #os.mkdir(os.path.join(para_data['work_dir'],'shell',sp))
        shell_path=os.path.join(para_data['work_dir'],'shell','step1',sp,sp+'_get_reads.sh')
        result_path=os.path.join(para_data['work_dir'],'step2',sp)
        with open(shell_path,'w') as SHELL:
            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
            print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/01_get_reads.py'+' '+kraken_file+' '+sp+' '+result_path+' &&'
            #print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+'_reads_r_1.list > '+result_path+'/'+sp+'_reads_r_1.list &&'
            print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+'_reads_r_1.list >'+result_path+'/'+sp+'_reads_r_1.list.fq'+ ' &&'
            print >>SHELL,'gzip '+result_path+'/'+sp+'_reads_r_1.list.fq'+' &&'
            #print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+'_reads_r_1.list > '+result_path+'/'+sp+'_reads_r_2.list'
            print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read2']+' '+result_path+'/'+sp+'_reads_r_2.list > '+result_path+'/'+sp+'_reads_r_2.list.fq'+' &&'
            print >>SHELL,'gzip '+result_path+'/'+sp+'_reads_r_2.list.fq'+' &&'
            print >>SHELL,"awk -F '#' '{print $2}' "+result_path+"/"+sp+"_reads_r_1.list|awk -F '/' '{print $1}' - |sort|uniq > "+result_path+'/'+sp+"_barcode.list"+' &&'
            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
        for z in final_process[sp]:
            if z=='all_barcode':
                shell_path=os.path.join(para_data['work_dir'],'shell',sp,sp+'_all_barcode.sh')
                result_path=os.path.join(para_data['work_dir'],sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    print >>SHELL,"grep '0_0_0' "+result_path+'/../'+sp+"_reads_r_1.list > "+result_path+'/'+sp+"_reads_0_0_0_r_1.list"+' &&'
                    print >>SHELL,"cp "+result_path+'/'+sp+"_reads_0_0_0_r_1.list "+result_path+'/'+sp+"_reads_0_0_0_r_2.list"+' &&'
                    print >>SHELL,"sed -i 's#0_0_0/1#0_0_0/2#g' "+result_path+'/'+sp+"_reads_0_0_0_r_2.list"+' &&'
                    print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_get_seq_from_barcode.py '+result_path+"/../"+sp+"_barcode.list "+para_data['work_dir']+"/kraken/all_seq_id.list "+result_path+' &&'
                    print >>SHELL,"cat "+result_path+'/'+sp+"_reads_0_0_0_r_1.list "+result_path+'/'+sp+"_barcode.list_r_1.list > "+result_path+'/'+sp+"_barcode_combine_r_1.list"+' &&'
                    print >>SHELL,"cat "+result_path+"/"+sp+"_reads_0_0_0_r_2.list "+result_path+'/'+sp+"_barcode.list_r_2.list > "+result_path+'/'+sp+"_barcode_combine_r_2.list"+' &&'
                    print >>SHELL, para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+"_barcode_combine_r_1.list > "+result_path+'/'+sp+"_all_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_all_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL, para_data['seqkit_path']+' subseq '+para_data['raw_data']['read2']+' '+result_path+'/'+sp+"_barcode_combine_r_2.list > "+result_path+'/'+sp+"_all_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_all_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"
            elif z=='unique_barcode':
                shell_path=os.path.join(para_data['work_dir'],'shell',sp,sp+'_uniq_barcode.sh')
                result_path=os.path.join(para_data['work_dir'],sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    #print >>SHELL,"cat "+result_path+"/../*_barcode.list > "+result_path+'/all_sample_barcode.list'+' &&'
                    #print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/02_choose_uniq_barcode.py '+result_path+'/all_sample_barcode.list '+result_path+'/../'+sp+'_barcode.list '+sp+' '+result_path+' &&'
                    #print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_create_combine_uniq_read_list.py '+para_data['work_dir']+'/sample_list '+result_path+' '+para_data['raw_data']['read1']+' '+result_path+' &&'
                    print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_create_combine_uniq_read_list.py '+para_data['work_dir']+'/kraken/all_sample_uniq_barcode_reads.list '+para_data['work_dir']+'/kraken/all_seq_id.list '+sp +' '+result_path+'/../ '+result_path+' &&'
                    print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+"_uniq_barcode_combine_r_1.list > "+result_path+'/'+sp+"_unique_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_unique_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read2']+' '+result_path+'/'+sp+"_uniq_barcode_combine_r_2.list > "+result_path+'/'+sp+"_unique_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_unique_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"
            elif z=='all_read':
                shell_path=os.path.join(para_data['work_dir'],'shell',sp,sp+'_all_read.sh')
                result_path=os.path.join(para_data['work_dir'],sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    print >>SHELL,'ln -s '+para_data['work_dir']+'/'+sp+'/'+sp+'_reads_r_1.list.fq.gz '+result_path+'/'+sp+'_all_read_list_r_1.list.fq.gz'+' &&'
                    print >>SHELL,'ln -s '+para_data['work_dir']+'/'+sp+'/'+sp+'_reads_r_2.list.fq.gz '+result_path+'/'+sp+'_all_read_list_r_2.list.fq.gz'+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"

def stlfrqc(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            shell_path=os.path.join(para_data['work_dir'],'shell',sp,stra,sp+'_stlfrqc.sh')
            result_path=os.path.join(para_data['work_dir'],sp,stra,'stlfrqc')
            with open(shell_path,'w') as SHELL:
                print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                print >>SHELL,'cd '+result_path+' &&'
                print >>SHELL,para_data['stLFRQC']['path']+' --bwa '+para_data['stLFRQC']['bwa']+' --samtools '+para_data['stLFRQC']['samtools']+' --python3 '+para_data['stLFRQC']['python3']+' --thread '+str(para_data['stLFRQC']['thread'])+' --gap_threshold '+str(para_data['stLFRQC']['gap_threshold'])+' --ref '+para_data['stLFRQC']['ref_dir']+'/'+sp+'_genomic.fa --read1 '+result_path+'/../'+sp+'_'+stra+'_list_r_1.list.fq.gz --read2 '+result_path+'/../'+sp+'_'+stra+'_list_r_2.list.fq.gz'+' &&'
                #print >>SHELL,para_data['bwa']['path']+' mem -t '+str(para_data['bwa']['thread'])+' -M '+para_data['bwa']['ref_dir']+'/'+sp+'_genomic.fa '+' '+result_path+'/../'+sp+'_'+stra+'_combine_r_1.list.fq.gz '+result_path+'/../'+sp+'_'+stra+'_combine_r_2.list.fq.gz 1>'+result_path+'/'+sp+'_'+stra+'.sam 2>'+result_path+'/'+sp+'_'+stra+'_bwa_map.log'+' &&'
                print >>SHELL,para_data['stLFRQC']['samtools']+' view -bS '+result_path+'/'+'temp.01.fixmate.sort.markdup.sam > '+result_path+'/'+sp+'_'+stra+'.bam'+' &&'
                print >>SHELL,'rm '+result_path+'/temp.01.fixmate.sort.markdup.sam'+' &&'
                print >>SHELL,para_data['stLFRQC']['samtools']+' sort --threads '+str(para_data['stLFRQC']['thread'])+' '+result_path+'/'+sp+'_'+stra+'.bam >'+result_path+'/'+sp+'_'+stra+'_sort.bam'+' &&'
                print >>SHELL,'rm '+result_path+'/'+sp+'_'+    stra+'.bam'+' &&'
                print >>SHELL,para_data['stLFRQC']['samtools']+' depth -a --reference '+para_data['stLFRQC']['ref_dir']+'/'+sp+'_genomic.fa '+result_path+'/'+sp+'_'+stra+'_sort.bam > '+result_path+'/'+sp+'_'+stra+'_sort.bam.flagstat'+' &&'
                print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/cal_coverage.py '+result_path+'/'+sp+'_'+stra+'_sort.bam.flagstat'+' &&'
                #print >>SHELL,'rm '+result_path+'/temp.*'+' &&'
                print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def denovo(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if dd=='idba' or dd=='supernova':
                    shell_path=os.path.join(para_data['work_dir'],'shell',sp,stra,sp+'_'+dd+'.sh')
                    result_path=os.path.join(para_data['work_dir'],sp,stra,dd)
                    with open(shell_path,'w') as SHELL:
                        if dd=='idba':
                            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                            print >>SHELL,'gzip -dc '+result_path+'/../'+sp+'_'+stra+'_list_r_1.list.fq.gz > '+result_path+'/'+sp+'_'+stra+'_list_r_1.list.fq'+' &&'
                            print >>SHELL,'gzip -dc '+result_path+'/../'+sp+'_'+stra+'_list_r_2.list.fq.gz > '+result_path+'/'+sp+'_'+stra+'_list_r_2.list.fq'+' &&'
                            print >>SHELL,os.path.join(os.path.dirname(para_data['denovo']['idba']['path']),'fq2fa')+' --merge '+result_path+'/'+sp+'_'+stra+'_list_r_1.list.fq '+result_path+'/'+sp+'_'+stra+'_list_r_2.list.fq '+result_path+'/'+sp+'_'+stra+'_merge.fq'+' &&'
                            print >>SHELL,para_data['denovo']['idba']['path']+' -r '+result_path+'/'+sp+'_'+stra+'_merge.fq -o '+result_path+' --mink 23 --maxk 83  --step 20 --num_threads '+str(para_data['denovo']['idba']['thread'])+' --pre_correction'+' &&'
                            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'                    
                        elif dd=='supernova':
                            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                            print >>SHELL,'cd '+result_path
                            print >>SHELL,para_data['python_path']+' '+para_data['denovo']['supernova']['path']+' -f 0 -m 1 -supernova /dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/xumengyang/software/supernova4stLFR/ -s /dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/xumengyang/software/stlfr2supernova_pipeline/clean_stLFR_data2supernova/ -o '+result_path+' -n '+sp+' -r1 '+result_path+'/../'+sp+'_'+stra+'_list_r_1.list.fq.gz -r2 '+result_path+'/../'+sp+'_'+stra+'_list_r_2.list.fq.gz'+' &&'
                            print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def evaluation(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if dd=='idba' or dd=='supernova':
                    shell_path=os.path.join(para_data['work_dir'],'shell',sp,stra,sp+'_'+dd+'_quast.sh')
                    result_path=os.path.join(para_data['work_dir'],sp,stra,'quast',dd)
                    with open(shell_path,'w') as SHELL:
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                        if dd=='supernova':
                            print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                            print >>SHELL,para_data['denovo']['quast']['path']+' -r '+para_data['denovo']['quast']['ref_dir']+'/'+sp+'_genomic.fa'+' -t '+str(para_data['denovo']['quast']['thread'])+' -o '+result_path+' '+result_path+'/../../supernova/'+sp+'_supernova_result.fasta.gz'+' &&'
                        elif dd=='idba':
                            print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                            print >>SHELL,para_data['denovo']['quast']['path']+' -r '+para_data['denovo']['quast']['ref_dir']+'/'+sp+'_genomic.fa'+' -t '+str(para_data['denovo']['quast']['thread'])+' -o '+result_path+' '+result_path+'/../../idba/'+'scaffold.fa'+' &&'
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def denovo_filt(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if dd=='idba' or dd=='supernova':
                    shell_path=os.path.join(para_data['work_dir'],'shell',sp,stra,sp+'_'+dd+'_filt_by_quast.sh')
                    result_path=os.path.join(para_data['work_dir'],sp,stra,'filt',dd)
                    with open(shell_path,'w') as SHELL:
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                        print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                        if dd=='supernova':
                            print >>SHELL,'gzip -dc '+result_path+'/../../supernova/'+sp+'_supernova_result.fasta.gz > '+result_path+'/'+sp+'_supernova_result.fasta'+' &&'
                            print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/acquire_scaffoldname_from_quast.py -t supernova -s '+result_path+'/'+sp+'_supernova_result.fasta -a '+result_path+'/../../quast/supernova/contigs_reports/'+'all_alignments_'+sp+'_supernova_result.tsv -o '+result_path+'/'+sp+'_supernova_filt'+' &&'
                        elif dd=='idba':
                            print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/acquire_scaffoldname_from_quast.py -t idba -s '+result_path+'/../../idba/scaffold.fa -a '+result_path+'/../../quast/idba/contigs_reports/'+'all_alignments_scaffold.tsv -o '+result_path+'/'+sp+'_idba_filt'+' &&'
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def main(para_data):
    print 'run config check'
    config_check_and_get_info(para_data)
    print 'create work dir'
    mk_dir(final_process)
    try:
        para_data['kraken_result']
    except:
        try:
            para_data['kraken']
        except:
            print 'no kraken or kraken_result is set, check it please'
            sys.exit()
        else:
            print 'no kraken result provide, create run_kraken script first'
            run_kraken(para_data)
            #para_data=run_kraken(para_data)
    else:
        print 'kraken result has been created before, skip create run_kraken script'
    try:
        para_data['abundance']
    except:
        print 'no set abundance process, skip this step'
    else:
        abundance(para_data)
    print 'create classify kraken result script'
    classify_kraken(final_process)
    print 'create get reads script'

    print 'finish step1 script create, before run step2, you can change the sample list in '+para_data['work_dir']+'/sample_list to run step2.'
    #get_reads(final_process)
    #try:
    #    para_data['stLFRQC']
    #except:
    #    print "not set stLFRQC process, skip this step"
    #else:
    #    print 'create stLFRQC script'
    #    stlfrqc(final_process)
    #try:
    #    para_data['denovo']
    #except:
    #    print "not set denovo process,skip this step"
    #else:
    #    print 'create denovo script'
    #    denovo(final_process)
    #try:
    #    para_data['denovo']['quast']
    #except:
    #    print "not set evaluation process,skip this step"
    #else:
    #    print 'create denovo evaluation script'
    #    evaluation(final_process)
    #try:
    #    para_data['denovo']['filt']
    #except:
    #    print "not set denovo reslut file process,skip this step"
    #else:
    #    print 'create denovo filt script'
    #    denovo_filt(final_process)
    #print 'all step done'
 
if __name__=='__main__':
    with open(sys.argv[1]) as conf:
        para_data=yaml.load(conf)
    main(para_data)
