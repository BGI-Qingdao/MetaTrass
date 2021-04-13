#-*-coding:utf-8-*-
###usage:python2 get_reads_abundance.py classify_out.C outdir ref_genome_dir taxonomy_info
import sys
import random
import os

species={}
genus={}
family={}
node_file=open(sys.argv[4])
for line in node_file:
    line=line.strip().split('\t')
    if line[4]=='species':
        species[line[0]]=''
    else:
        pass
#    elif line[4]=='genus':
#        genus[line[0]]=''
#    elif line[4]=='family':
#        family[line[4]]=''
node_file.close()


num={}
infile=open(sys.argv[1])
for line in infile:
    line=line.strip().split('\t')
    taxid=line[2]
    id=line[1]
    if taxid not in num:
        num[taxid]=[id]
    else:
        num[taxid].append(id)
infile.close()
outfile=open(sys.argv[2]+'/all_taxid_abundance.list','w')
#print >>outfile,'taxid'+'\t'+'read_pairs'+'\t'+'level'
for ii in num:
    if ii in species:
        print >>outfile,ii+'\t'+str(len(num[ii]))+'\t'+'species'
    elif ii in genus:
        print >>outfile,ii+'\t'+str(len(num[ii]))+'\t'+'genus'
    elif ii in family:
        print >>outfile,ii+'\t'+str(len(num[ii]))+'\t'+'family'
    else:
        pass
outfile.close()
os.system('echo taxid"\t"reads_num"\t"level >'+sys.argv[2]+'/all_taxid_abundance.sort.list')
os.system('sort -n -k2 -r '+sys.argv[2]+'/all_taxid_abundance.list >> '+sys.argv[2]+'/all_taxid_abundance.sort.list')
os.system('rm '+sys.argv[2]+'/all_taxid_abundance.list')
abun=open(sys.argv[2]+'/all_taxid_abundance.sort.list')
outs=open(sys.argv[2]+'/all_taxid_abundance.sort.matrix','w')
print >>outs,'taxid'+'\t'+'read_pairs'+'\t'+'genome_size'+'\t'+'estimate_abundance'
for line in abun:
    line=line.strip().split('\t')
    if line[0]!='taxid' and line[0] in species:
        tax=line[0];reads=int(line[1])
        geno_name=tax
        geno_size=''
        try:
            geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'.fa')
        except:
            try:
                geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'.fna')
            except:
                try:
                    geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'.fasta')
                except:
                    try:
                        geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'_genomic.fna')
                    except:
                        try:
                            geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'_genomic.fa')
                        except:
                            try:
                                geno_size=os.path.getsize(sys.argv[3]+'/'+geno_name+'_genomic.fasta')
                            except:
                                print 'not find genome file for '+geno_name+', skip the calculate abundance process'
        if geno_size!='':
            abundance=format(int(len(num[tax]))*2*100/float(geno_size),'.4f')
            print >>outs,tax+'\t'+str(reads)+'\t'+str(geno_size)+'\t'+str(abundance)
        else:
             print >>outs,tax+'\t'+str(reads)+'\t'+'no_ref_genome'+'\t'+'no_estimate_abundance'
abun.close()
outs.close()
