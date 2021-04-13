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
    
    #if os.path.exists(work_dir):
    #    shutil.rmtree(work_dir)
    #os.mkdir(work_dir)

    global sample_list
    sample_list=[]
    
    try:
        inputs=open(work_dir+'/sample_list')
    except:
        print 'there is no file: sample_list in dicectory: '+work_dir
        sys.exit()
    else:
        for i in inputs:
            sample_list.append(i.strip())
        inputs.close()

    if strategy=='all':
        strategy=['all_read','all_barcode','unique_barcode']
    elif len(strategy.strip().split(';'))==2 or len(strategy.strip().split(';'))==3:
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
            if 'supernova' in para_data['denovo'] or 'idba' in para_data['denovo']:
                process.append('quast')
            else:
                print 'no supernova or idba is set to run before, can not run quast'
                sys.exit()
        try:
            para_data['denovo']['filt']
        except:
            pass
        else:
            if 'quast' in para_data['denovo']:
                process.append('filt')
            else:
                print 'no quast is set to run before, filt rely on the quast\'s result'
                sys.exit()
    
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
    if os.path.exists( os.path.join(work_dir,'shell','step2') ):
        pass
    else:
        os.mkdir(os.path.join(work_dir,'shell','step2')) 
    if os.path.exists( os.path.join(work_dir,'result','step2') ):
        pass
    else:
        os.mkdir(os.path.join(work_dir,'result','step2')) 
    #os.mkdir(os.path.join(work_dir,'kraken'))
    #os.mkdir(os.path.join(work_dir,'shell'))
    #os.system('cp '+para_data['script_path']+'/remove_no_need_dir.py '+os.path.join(work_dir,'shell'))
    for sample in final_process:
        if os.path.exists(os.path.join(work_dir,'shell','step2',str(sample))):
            shutil.rmtree(os.path.join(work_dir,'shell','step2',str(sample)))
            os.mkdir(os.path.join(work_dir,'shell','step2',str(sample)))
	else:
            os.mkdir(os.path.join(work_dir,'shell','step2',str(sample)))
        if os.path.exists(os.path.join(work_dir,'result','step2',str(sample))):
            shutil.rmtree(os.path.join(work_dir,'result','step2',str(sample)))
            os.mkdir(os.path.join(work_dir,'result','step2',str(sample)))
	else:
            os.mkdir(os.path.join(work_dir,'result','step2',str(sample)))
        for strategy in final_process[sample]:
            if os.path.exists(os.path.join(work_dir,'result','step2',str(sample),strategy)):
                shutil.rmtree(os.path.join(work_dir,'result','step2',str(sample),strategy))
                os.mkdir(os.path.join(work_dir,'result','step2',str(sample),strategy))
            else:
                os.mkdir(os.path.join(work_dir,'result','step2',str(sample),strategy))
            if os.path.exists(os.path.join(work_dir,'shell','step2',str(sample),strategy)):
                shutil.rmtree(os.path.join(work_dir,'shell','step2',str(sample),strategy))
                os.mkdir(os.path.join(work_dir,'shell','step2',str(sample),strategy))
            else:
                os.mkdir(os.path.join(work_dir,'shell','step2',str(sample),strategy))
            for process in final_process[sample][strategy]:
                if os.path.exists(os.path.join(work_dir,'shell','step2',str(sample),strategy,process)):
                    shutil.rmtree(os.path.join(work_dir,'shell','step2',str(sample),strategy,process))
                    os.mkdir(os.path.join(work_dir,'shell','step2',str(sample),strategy,process))
                else:
                    os.mkdir(os.path.join(work_dir,'shell','step2',str(sample),strategy,process))
                if os.path.exists(os.path.join(work_dir,'result','step2',str(sample),strategy,process)):
                    shutil.rmtree(os.path.join(work_dir,'result','step2',str(sample),strategy,process))
                    os.mkdir(os.path.join(work_dir,'result','step2',str(sample),strategy,process))
                else:
                    os.mkdir(os.path.join(work_dir,'result','step2',str(sample),strategy,process))
    
def run_kraken(para_data):
    shell_path=os.path.join(para_data['work_dir'],'shell','run_kraken.sh') 
    result_path=os.path.join(para_data['work_dir'],'kraken')
    with open(shell_path,'w') as SHELL:
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
        print >>SHELL,para_data['kraken']['path']+' --threads '+str(para_data['kraken']['thread'])+' --gzip-compressed --paired --db '+para_data['kraken']['taxonomy_path']+' --output '+result_path+'/kraken_result.C --report '+result_path+'/kraken_result.report '+para_data['raw_data']['read1']+' '+para_data['raw_data']['read2']+' &&'
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
    para_data['kraken_result']=result_path+'/kraken_result.C'
    #return para_data

def classify_kraken(final_process):
    kraken_result=para_data['kraken_result']
    final_filename='final_kraken_result.C'
    read1=para_data['raw_data']['read1']
    shell_path=os.path.join(para_data['work_dir'],'shell','classify_kraken_result.sh')
    result_path=os.path.join(para_data['work_dir'],'kraken')
    with open(shell_path,'w') as SHELL:
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
        print >>SHELL,'ln -s '+kraken_result+' '+result_path+'/'+final_filename+' &&'
        print >>SHELL,"awk -F '\\t' '{if($3!=0)print $0}' "+os.path.join(result_path,final_filename)+" > "+os.path.join(result_path,final_filename+'_classify.list')+" &&"
        print >>SHELL,"awk -F '\\t' '{if($3==0)print $0}' "+os.path.join(result_path,final_filename)+" > "+os.path.join(result_path,final_filename+'_unclassify.list')+" &&"
        print >>SHELL,"awk -F \\t '{print $2}' "+os.path.join(result_path,final_filename)+' > '+os.path.join(result_path,"all_seq_id.list")+' &&'
        #print >>SHELL,"less -S "+read1+"| awk -F '' '{if($1==\"@\" && $2==\"C\" && $3==\"L\")print $0}' - | awk -F ' ' '{print $1}' - >"+os.path.join(result_path,"all_seq_id.list")+' &&'
        #print >>SHELL,"awk -F '#' '{print $2}' "+result_path+"/all_seq_id.list |awk -F '/' '{print $1}' - > "result_path+"/all_seq_barcode.list"+' &&'
        print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/get_all_sample_uniq_barcode_reads.py '+os.path.join(result_path,final_filename+'_classify.list')+' '+result_path+' &&'
        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'

def abundance(para_data):
    kraken_result=para_data['work_dir']+'/kraken/final_kraken_result.C_classify.list'
    ref_dir=para_data['abundance']['ref_dir']
    shell_path=os.path.join(para_data['work_dir'],'shell','kraken_result_abundance.sh')  
    result_path=os.path.join(para_data['work_dir'],'kraken')
    with open(shell_path,'w') as SHELL:
       print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
       print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/get_reads_abundance.py '+kraken_result+' '+result_path+' '+ref_dir
       print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
        
def get_reads(final_process):
    kraken_file=os.path.join(para_data['work_dir'],'result','step1','final_kraken_result.C_classify.list')
    sample_file=para_data['work_dir']+'/sample_list'
    for sp in final_process:
        #sp=str(sp)
        #os.mkdir(os.path.join(para_data['work_dir'],'shell',sp))
        shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_get_reads.sh')
        result_path=os.path.join(para_data['work_dir'],'result','step2',sp)
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
            shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+z+'_pipeline.sh')
            SHELL_PIPE=open(shell_pipeline_path,'a+')
            if z=='all_barcode':
                shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+z+'.sh')
                result_path=os.path.join(para_data['work_dir'],'result','step2',sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    print >>SHELL,"grep '0_0_0' "+result_path+'/../'+sp+"_reads_r_1.list > "+result_path+'/'+sp+"_reads_0_0_0_r_1.list"+' &&'
                    print >>SHELL,"cp "+result_path+'/'+sp+"_reads_0_0_0_r_1.list "+result_path+'/'+sp+"_reads_0_0_0_r_2.list"+' &&'
                    print >>SHELL,"sed -i 's#0_0_0/1#0_0_0/2#g' "+result_path+'/'+sp+"_reads_0_0_0_r_2.list"+' &&'
                    print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_get_seq_from_barcode.py '+result_path+"/../"+sp+"_barcode.list "+para_data['work_dir']+"result/step1/all_seq_id.list "+result_path+' &&'
                    print >>SHELL,"cat "+result_path+'/'+sp+"_reads_0_0_0_r_1.list "+result_path+'/'+sp+"_barcode.list_r_1.list > "+result_path+'/'+sp+"_barcode_combine_r_1.list"+' &&'
                    print >>SHELL,"cat "+result_path+"/"+sp+"_reads_0_0_0_r_2.list "+result_path+'/'+sp+"_barcode.list_r_2.list > "+result_path+'/'+sp+"_barcode_combine_r_2.list"+' &&'
                    print >>SHELL, para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+"_barcode_combine_r_1.list > "+result_path+'/'+sp+"_all_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_all_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL, para_data['seqkit_path']+' subseq '+para_data['raw_data']['read2']+' '+result_path+'/'+sp+"_barcode_combine_r_2.list > "+result_path+'/'+sp+"_all_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_all_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"
            elif z=='unique_barcode':
                shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+z+'.sh')
                result_path=os.path.join(para_data['work_dir'],'result','step2',sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    #print >>SHELL,"cat "+result_path+"/../*_barcode.list > "+result_path+'/all_sample_barcode.list'+' &&'
                    #print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/02_choose_uniq_barcode.py '+result_path+'/all_sample_barcode.list '+result_path+'/../'+sp+'_barcode.list '+sp+' '+result_path+' &&'
                    #print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_create_combine_uniq_read_list.py '+para_data['work_dir']+'/sample_list '+result_path+' '+para_data['raw_data']['read1']+' '+result_path+' &&'
                    print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/03_create_combine_uniq_read_list.py '+para_data['work_dir']+'/result/step1/all_sample_uniq_barcode_reads.list '+para_data['work_dir']+'/result/step1/all_seq_id.list '+sp+' '+result_path+'/../ '+result_path+' &&'
                    print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read1']+' '+result_path+'/'+sp+"_uniq_barcode_combine_r_1.list > "+result_path+'/'+sp+"_unique_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_unique_barcode_list_r_1.list.fq"+' &&'
                    print >>SHELL,para_data['seqkit_path']+' subseq '+para_data['raw_data']['read2']+' '+result_path+'/'+sp+"_uniq_barcode_combine_r_2.list > "+result_path+'/'+sp+"_unique_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"gzip "+result_path+'/'+sp+"_unique_barcode_list_r_2.list.fq"+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"
            elif z=='all_read':
                shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+z+'.sh')
                result_path=os.path.join(para_data['work_dir'],'result','step2',sp,z)
                with open(shell_path,'w') as SHELL:
                    print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                    print >>SHELL,'ln -s '+para_data['work_dir']+'/'+'result/step2/'+sp+'/'+sp+'_reads_r_1.list.fq.gz '+result_path+'/'+sp+'_all_read_list_r_1.list.fq.gz'+' &&'
                    print >>SHELL,'ln -s '+para_data['work_dir']+'/'+'result/step2/'+sp+'/'+sp+'_reads_r_2.list.fq.gz '+result_path+'/'+sp+'_all_read_list_r_2.list.fq.gz'+' &&'
                    print >>SHELL,"echo --- "+os.path.basename(shell_path)+" end at `date` ---"
            print >>SHELL_PIPE,'sh '+shell_path+' &&'
            SHELL_PIPE.close()
 
def stlfrqc(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+stra+'_pipeline.sh')
            shell_path=os.path.join(para_data['work_dir'],'shell', 'step2',sp,stra,sp+'_stlfrqc.sh')
            result_path=os.path.join(para_data['work_dir'], 'result','step2',sp,stra,'stlfrqc')
            SHELL_PIPE=open(shell_pipeline_path,'a+')
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
            print >>SHELL_PIPE,'sh '+shell_path+' &&'
            SHELL_PIPE.close()

def denovo(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if dd=='idba' or dd=='supernova':
                    shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+stra+'_pipeline.sh')
                    SHELL_PIPE=open(shell_pipeline_path,'a+')
                    shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,stra,sp+'_'+dd+'.sh')
                    result_path=os.path.join(para_data['work_dir'],'result','step2', sp,stra,dd)
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
                    print >>SHELL_PIPE,'sh '+shell_path+' &&'
                    SHELL_PIPE.close()

def evaluation(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if dd=='idba' or dd=='supernova':
                    shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+stra+'_pipeline.sh')
                    SHELL_PIPE=open(shell_pipeline_path,'a+')
                    shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,stra,sp+'_'+dd+'_quast.sh')
                    result_path=os.path.join(para_data['work_dir'], 'result','step2' ,sp,stra,'quast',dd)
                    with open(shell_path,'w') as SHELL:
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                        if dd=='supernova':
                            print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                            print >>SHELL,para_data['denovo']['quast']['path']+' -r '+para_data['denovo']['quast']['ref_dir']+'/'+sp+'_genomic.fa'+' -t '+str(para_data['denovo']['quast']['thread'])+' -o '+result_path+' '+result_path+'/../../supernova/'+sp+'_supernova_result.fasta.gz'+' &&'
                        elif dd=='idba':
                            print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                            print >>SHELL,para_data['denovo']['quast']['path']+' -r '+para_data['denovo']['quast']['ref_dir']+'/'+sp+'_genomic.fa'+' -t '+str(para_data['denovo']['quast']['thread'])+' -o '+result_path+' '+result_path+'/../../idba/'+'scaffold.fa'+' &&'
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
                    print >>SHELL_PIPE,'sh '+shell_path+' &&'
                    SHELL_PIPE.close()

def denovo_filt(final_process):
    obj=para_data['denovo']['filt']['object']
    obj_list=[]
    if obj!='all' and obj!='supernova' and obj!='idba':
        print 'wrong donovo filt object set, only can be set as all/supernova/idba'
        sys.exit()
    if obj=='all':
        obj_list=['supernova','idba']
    else:
        obj_list=[obj]
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                if (dd=='idba' or dd=='supernova') and dd in obj_list:
                    shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+stra+'_pipeline.sh')
                    SHELL_PIPE=open(shell_pipeline_path,'a+')
                    shell_path=os.path.join(para_data['work_dir'],'shell','step2',sp,stra,sp+'_'+dd+'_filt_by_quast.sh')
                    result_path=os.path.join(para_data['work_dir'],'result','step2', sp,stra,'filt',dd)
                    with open(shell_path,'w') as SHELL:
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' start at `date` ---'
                        print >>SHELL,'if [ ! -d '+result_path+' ];then mkdir '+result_path+';fi'+' &&'
                        if dd=='supernova':
                            print >>SHELL,'gzip -dc '+result_path+'/../../supernova/'+sp+'_supernova_result.fasta.gz > '+result_path+'/'+sp+'_supernova_result.fasta'+' &&'
                            print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/acquire_scaffoldname_from_quast.py -t supernova -s '+result_path+'/'+sp+'_supernova_result.fasta -a '+result_path+'/../../quast/supernova/contigs_reports/'+'all_alignments_'+sp+'_supernova_result.tsv -o '+result_path+'/'+sp+'_supernova_filt'+' &&'
                            print >>SHELL,'rm '+result_path+'/'+sp+'_supernova_result.fasta'+' &&'
                        elif dd=='idba':
                            print >>SHELL,para_data['python_path']+' '+para_data['script_path']+'/acquire_scaffoldname_from_quast.py -t idba -s '+result_path+'/../../idba/scaffold.fa -a '+result_path+'/../../quast/idba/contigs_reports/'+'all_alignments_scaffold.tsv -o '+result_path+'/'+sp+'_idba_filt'+' &&'
                        print >>SHELL,'echo --- '+os.path.basename(shell_path)+' end at `date` ---'
                    print >>SHELL_PIPE,'sh '+shell_path +' &&'
                    SHELL_PIPE.close()
                else:
                    pass
                   
def del_end(final_process):
    for sp in final_process:
        for stra in final_process[sp]:
            for dd in final_process[sp][stra]:
                shell_pipeline_path=os.path.join(para_data['work_dir'],'shell','step2',sp,sp+'_'+stra+'_pipeline.sh')
                #SHELL_PIPE=open(shell_pipeline_path,'a+')
                os.system("sed -i '$s#&&##' "+shell_pipeline_path)

def main(para_data):
    config_check_and_get_info(para_data)
    print 'create work dir'
    mk_dir(final_process)
    #try:
    #    para_data['kraken_result']
    #except:
    #    try:
    #        para_data['kraken']
    #    except:
    #        print 'no kraken or kraken_result is set, check it please'
    #        sys.exit()
    #    else:
    #        print 'no kraken result provide, create run_kraken script first'
    #        run_kraken(para_data)
            #para_data=run_kraken(para_data)
    #else:
    #    print 'kraken result has been created before, skip create run_kraken script'
    #try:
    #    para_data['abundance']
    #except:
    #    print 'no set abundance process, skip this step'
    #else:
    #    abundance(para_data)
    #print 'create classify kraken result script'
    #classify_kraken(final_process)
    #print 'create get reads script'
    get_reads(final_process)
    print 'create get reads script'
    try:
        para_data['stLFRQC']
    except:
        print "not set stLFRQC process, skip this step"
    else:
        print 'create stLFRQC script'
        stlfrqc(final_process)
    try:
        para_data['denovo']
    except:
        print "not set denovo process,skip this step"
    else:
        print 'create denovo script'
        denovo(final_process)
    try:
        para_data['denovo']['quast']
    except:
        print "not set evaluation process,skip this step"
    else:
        print 'create denovo evaluation script'
        evaluation(final_process)
    try:
        para_data['denovo']['filt']
    except:
        print "not set denovo reslut file process,skip this step"
    else:
        print 'create denovo filt script'
        denovo_filt(final_process)
    del_end(final_process)
    print 'all step done'
 
if __name__=='__main__':
    with open(sys.argv[1]) as conf:
        global para_data
        para_data=yaml.load(conf)
    main(para_data)
