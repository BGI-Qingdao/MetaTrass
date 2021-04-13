#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re, os, sys, time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-sample', help='Name: sample name',required=True, type=str)
parser.add_argument('-fq1', help='Data: PE1 fastq gzip file required', required=True, type=str)
parser.add_argument('-fq2', help='Data: PE2 fastq gzip file required', required=True, type=str)
parser.add_argument('-outdir', help='Dirs: Store the files ', required=True, type=str)

parser.add_argument('-label', help='Labels: read query with co-barcode labels', default='stlfr',required=True, type=str)

parser.add_argument('-min_depth', help='Depth: Minium Depth ', default = 10, required=True, type=str)
parser.add_argument('-max_depth', help='Depth: Maxium Depth ', default = 300, required=True, type=str)
parser.add_argument('-kraken_db', help='DBdir: DB build on Kraken', required=True, type=str)
parser.add_argument('-kraken_fa', help='DBdir: DB build on Kraken', required=True, type=str)
parser.add_argument('-genome_sz', help='DBdir: Genome size data', required=True, type=str)

parser.add_argument('-threads', help='Threads: maxium threads',default = 20, required=True, type=str)
parser.add_argument('-strategy', help='Strategy: all read & all barcode', default = 'both', required=True, type=str)
parser.add_argument('-idba_ud', help='Assembly: IDBA_UD', default = 'yes', required=True, type=str)
parser.add_argument('-supernova', help='Assembly: Supernova', default = 'yes', required=True, type=str)
parser.add_argument('-quast', help='Assessment: Quast launch', default = 'yes', required=True, type=str)
parser.add_argument('-checkm', help='Assessment: CheckM launch', default = 'yes', required=True, type=str)

parser.add_argument('-IDY', help='Assessment: min-identity (0.5-1)', default = 'yes', required=True, type=str)
parser.add_argument('-PCT', help='Assessment: consensus sequence percentage %(85-100)', default = 'yes', required=True, type=str)

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
dirname = dirname + '/..'
args = parser.parse_args()

def mkdirIfNotExists(filename):
	if os.path.exists(filename):
		pass
	else:
		os.mkdir(filename)

filefold = args.outdir
mkdirIfNotExists(filefold)

commandsh_dir = filefold +  '/all_command_shell/'
mkdirIfNotExists(commandsh_dir)

cleandata_dir = filefold + '/step1_cleandata/'
mkdirIfNotExists(cleandata_dir)

taxonomy_dir = filefold + '/step2_taxonomy/'
mkdirIfNotExists(taxonomy_dir)

assembly_dir = filefold + '/step3_assembly/'
mkdirIfNotExists(assembly_dir)

assessment_dir = filefold + '/step4_assessment/'
mkdirIfNotExists(assessment_dir)

binfilter_dir = filefold + '/step5_binfilter/'
mkdirIfNotExists(binfilter_dir)

# step 0
def create_shell_script(function, shfile, command):
	start = 'echo --- '+ function + ' start at `date` ---'
	end = 'echo --- ' + function + ' end at `date` ---'
	sh = open(shfile, 'w')
	sh.write(start + '\n' + command + '\n' + end + '\n')
	sh.close()

# step 1 #################################################################################################
def stlfr_split_barcode_shell(shfile, split_barcodePL, barcode_list, rawfq1, rawfq2, sample, outdir):
	command1 = 'cd ' + outdir
	command2 = ' '.join(['perl', split_barcodePL, barcode_list, rawfq1, rawfq2, 'split_reads'  ])
	command = '\n'.join([command1, command2])
	create_shell_script( 'step1.1 stlfr_split_barcode', shfile, command)

def stlfr_data_clean_shell(shfile, barfq1, barfq2, soap_filter, soap_parameter, sample, outdir):
	lane_lst = open(outdir+'lane.lst', 'w')
	lane_lst.write('split_reads.1.fq.gz 0 0 10\nsplit_reads.2.fq.gz 0 0 10\n')
	lane_lst.close()

	stat_txt = open(outdir+'stat.txt', 'w')
	stat_txt.write('#raw_read_id    raw_read_pair_num       raw_read_length raw_base_num    low_qual_filter(%)      adapter_filter(%)       undersize_ins_filter(%)    duplicated_filter(%)    clean_read_pair_num     clean_read_length       clean_base_num')
	stat_txt.close()

	command1 = ' '.join(['cd', outdir])
	command2 = ' '.join([ soap_filter, soap_parameter, 'lane.lst', 'stat.txt'  ])
	command = '\n'.join([command1, command2])
	create_shell_script( 'step1.2 stlfr_data_clean', shfile, command)

# step 2 #################################################################################################
def run_kraken_shell(shfile, cleanfq1, cleanfq2, kraken, kraken_parameter, sample, outdir):
	command = ' '.join([ kraken,  kraken_parameter,  '--report', outdir+sample+'.R', '--output', outdir+sample+'.C', cleanfq1, cleanfq2 ])
	create_shell_script('step2.1 run_kraken', shfile, command)

def get_all_single_species_reads_list(shfile, splitterCC, species_genome_size, min_depth, limited_depth, kraken_C, outdir):
	command1 = ' '.join(['mkdir -p ' + outdir + ' && cd ' + outdir + ' && '])
	command2 = ' '.join([ splitterCC, species_genome_size, kraken_C ])
	create_shell_script( 'get_all_single_species_reads_list', shfile, command1 + command2)

def convert_single_species_fq_gz(shfile, seqtk, indir, outdir, readlist, cleanfq1, cleanfq2):
	fq1list	= outdir + readlist + '_list_1'
	fq2list = outdir + readlist + '_list_2'
	command1 = ' '.join([ 'awk', '\'{print $1"/1"}\'',  indir + readlist, '>', fq1list ])
	command2 = ' '.join([ 'awk', '\'{print $1"/2"}\'',  indir + readlist, '>', fq2list ])
	command3 = ' '.join([seqtk, 'subseq', cleanfq1, fq1list, '|gzip >', fq1list + '.fq.gz' ])
	command4 = ' '.join([seqtk, 'subseq', cleanfq2, fq2list, '|gzip >', fq2list + '.fq.gz' ])
	command5 = ' '.join([ 'rm', fq1list])
	command6 = ' '.join([ 'rm', fq2list])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	create_shell_script('convert_single_species_fq_gz', shfile, command)

def create_batch_fq_convert_sh(X10, X300, seqtk, indir, outdir, cleanfq1, cleanfq2):
	batchsh_dir = commandsh_dir + '/step2.3.convert_single_species_fq_sh/'
	mkdirIfNotExists(batchsh_dir)

	if len(X10) > 0:
		for i in X10:
			if args.strategy == 'both':
				allreadlist = '10X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X10_TID' + i + '_AR.sh'
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X10_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			elif args.strategy == 'allread':
				allreadlist = '10X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X10_TID' + i + '_AR.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
			elif args.strategy == 'allbarcode':
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X10_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 10X condition!!!')
	if len(X300) > 0:
		for i in X300:
			if args.strategy == 'both':
				allreadlist = '300X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X300_TID' + i + '_AR.sh'
				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X300_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			elif args.strategy == 'allread':
				allreadlist = '300X.id_' + i + '.allread.txt'
				shFileAR = batchsh_dir + 'step2.3_X300_TID' + i + '_AR.sh'
				convert_single_species_fq_gz(shFileAR, seqtk, indir, outdir, allreadlist, cleanfq1, cleanfq2)
			elif args.strategy == 'allbarcode':
				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				shFileAB = batchsh_dir + 'step2.3_X300_TID' + i + '_AB.sh'
				convert_single_species_fq_gz(shFileAB, seqtk, indir, outdir, allbarcodelist, cleanfq1, cleanfq2)
			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 300X condition!!!')

# step 3 #################################################################################################
##idba-ud assembly
def idba_assembly_shell(shfile, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, sample, outdir):
	idba_dir = outdir + '/idba-ud/' + sample
	command0 = ' '.join([ 'mkdir -p ', idba_dir, ' && cd ', idba_dir ])
	command1 = ' '.join([ 'gzip -dc', tssfq1, '>', idba_dir+'/idba.fq1' ])
	command2 = ' '.join([ 'gzip -dc', tssfq2, '>', idba_dir+'/idba.fq2' ])
	command3 = ' '.join([ fq2fa, '--merge', idba_dir+'/idba.fq1', idba_dir+'/idba.fq2', idba_dir+'/idba.merge.fq' ])
	command4 = ' '.join([ 'rm -f', idba_dir+'/idba.fq1', idba_dir+'/idba.fq2' ])
	command5 = ' '.join([ idba_ud, idba_parameter, '-r', idba_dir+'/idba.merge.fq', '-o', idba_dir ])
	command6 = ' '.join([ 'rm -f', idba_dir+'/*-*', idba_dir+'/idba.merge.fq', idba_dir+'/kmer' ])
	command = '\n'.join([ command0, command1, command2, command3, command4, command5, command6 ])
	create_shell_script('idba_assembly_shell', shfile, command)

def create_batch_idba_assembly_sh(X10, X300, indir, outdir, fq2fa, idba_ud, idba_parameter):
	batchsh_dir = commandsh_dir + '/step3.2.batch_idba_assembly_sh/'
	mkdirIfNotExists(batchsh_dir)
	if len(X10) > 0:
		for i in X10:
			if args.strategy == 'both':
				allreadlist = '10X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh_dir + 'step3.2_X10_TID' + i + '_AR.sh'
				idba_assembly_shell(shFileAR, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh_dir + 'step3.2_X10_TID' + i + '_AB.sh'
				idba_assembly_shell(shFileAB, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			elif args.strategy == 'allread':
				allreadlist = '10X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh_dir + 'step3.2_X10_TID' + i + '_AR.sh'
				idba_assembly_shell(shFileAR, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

			elif args.strategy == 'allbarcode':
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh_dir + 'step3.2_X10_TID' + i + '_AB.sh'
				idba_assembly_shell(shFileAB, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 10X condition!!!')
	if len(X300) > 0:
		for i in X300:
			if args.strategy == 'both':
				allreadlist = '300X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh_dir + 'step3.2_X300_TID' + i + '_AR.sh'
				idba_assembly_shell(shFileAR, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh_dir + 'step3.2_X300_TID' + i + '_AB.sh'
				idba_assembly_shell(shFileAB, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			elif args.strategy == 'allread':
				allreadlist = '300X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh_dir + 'step3.2_X300_TID' + i + '_AR.sh'
				idba_assembly_shell(shFileAR, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

			elif args.strategy == 'allbarcode':
				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh_dir + 'step3.2_X300_TID' + i + '_AB.sh'
				idba_assembly_shell(shFileAB, fq2fa, idba_ud, idba_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 300X condition!!!')
### supernova assembly
def supernova_assembly_shell(shfile, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, sample, outdir):
	supernova_dir = outdir + '/supernova/' + sample
	command1 = ' '.join([ 'mkdir -p ', supernova_dir, ' && cd ', supernova_dir ])
	command2 = ' '.join([ python2, supernovaPY, supernova_parameter, '-n', sample, '-r1', tssfq1, '-r2', tssfq2,'-o', supernova_dir ])
	command3 = ' '.join([ 'mv', 'supernova_outs/supernova_out.mri.tgz', './' ])
	command4 = ' '.join([ 'rf -rf', 'supernova_outs/' ])
	command5 = ' '.join([ 'gunzip -c', supernova_dir+'/'+sample+'_supernova_result.fasta.gz', '>', supernova_dir + '/scaffold.fa'])
	command = '\n'.join([ command1, command2, command3, command4, command5 ])
	create_shell_script( 'supernova_assembly_shell', shfile, command)

def create_batch_supernova_assembly_sh(X10, X300, python2, indir, outdir, supernovaPY, supernova_parameter):
	batchsh3_dir = commandsh_dir + '/step3.1.batch_supernova_assembly_sh/'
	mkdirIfNotExists(batchsh3_dir)
	if len(X10) > 0:
		for i in X10:
			if args.strategy == 'both':
				allreadlist = '10X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh3_dir + 'step3.1_X10_TID' + i + '_AR.sh'
				supernova_assembly_shell(shFileAR, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh3_dir + 'step3.1_X10_TID' + i + '_AB.sh'
				supernova_assembly_shell(shFileAB, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			elif args.strategy == 'allread':
				allreadlist = '10X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh3_dir + 'step3.1_X10_TID' + i + '_AR.sh'
				supernova_assembly_shell(shFileAR, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

			elif args.strategy == 'allbarcode':
				allbarcodelist = '10X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh3_dir + 'step3.1_X10_TID' + i + '_AB.sh'
				supernova_assembly_shell(shFileAB, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 10X condition!!!')
	if len(X300) > 0:
		for i in X300:
			if args.strategy == 'both':
				allreadlist = '300X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh3_dir + 'step3.1_X300_TID' + i + '_AR.sh'
				supernova_assembly_shell(shFileAR, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh3_dir + 'step3.1_X300_TID' + i + '_AB.sh'
				supernova_assembly_shell(shFileAB, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			elif args.strategy == 'allread':
				allreadlist = '300X.id_' + i + '.allread.txt'
				tssfq1 = indir + allreadlist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allreadlist + '_list_2' + '.fq.gz'
				shFileAR = batchsh3_dir + 'step3.1_X300_TID' + i + '_AR.sh'
				supernova_assembly_shell(shFileAR, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AR_' + i, outdir)

			elif args.strategy == 'allbarcode':
				allbarcodelist = '300X.id_' + i + '.allbarcode.txt'
				tssfq1 = indir + allbarcodelist + '_list_1' + '.fq.gz'
				tssfq2 = indir + allbarcodelist + '_list_2' + '.fq.gz'
				shFileAB = batchsh3_dir + 'step3.1_X300_TID' + i + '_AB.sh'
				supernova_assembly_shell(shFileAB, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, 'AB_' + i, outdir)

			else:
				print('Please select valid reads strategy')
	else:
		print('No species depth reach the 300X condition!!!')

# step 4 #################################################################################################
### quast bin result
def quast_bin_for_single_fasta(shfile, quastPY, taxidbin, taxidref, threads, outdir, IDY):
	command = ' '.join([ quastPY, '-r', taxidref, '-t', str(threads), '--min-identity', str(IDY), '-o', outdir, taxidbin ])
	create_shell_script("quast_bin_for_single_fasta", shfile, command)

### filter bin after quast
def create_binfilter_sh(shfile, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT):
	command = ' '.join(['python', binFilterPY, '-i', assemblyFa, '-o', filteredFa, '-r', refGenomeFa, '-q', quastAlnTsv, '-IDY', IDY, '-PCT', PCT])
	create_shell_script("filter_assmbled_species_bin", shfile, command)

def create_batch_quast_binfilter_sh(X10, X300, refGenomeDir, indir, assessment_dir, binfilter_dir, threads, quastPY, IDY, PCT):
	Xdepth = X10 + X300
	batchsh4_dir = commandsh_dir + '/step4.batch_assessment_sh/'
	batchsh5_dir = commandsh_dir + '/step5.batch_binfilter_sh/'
	mkdirIfNotExists(batchsh4_dir)
	mkdirIfNotExists(batchsh5_dir)
	idba_dir = assessment_dir + '/idba-ud/'
	supernova_dir = assessment_dir + '/supernova/'
	mkdirIfNotExists(idba_dir)
	mkdirIfNotExists(supernova_dir)
	mkdirIfNotExists(binfilter_dir + '/idba-ud/')
	mkdirIfNotExists(binfilter_dir + '/supernova/')

	if len(Xdepth) > 0:
		for i in Xdepth:
			if args.strategy == 'both':
				shFileAR = batchsh4_dir + 'step4.1_IDBA-UD_TID' + i + '_AR.sh'
				assemblyFa = indir + '/idba-ud/' +  'AR_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/idba-ud/' +  'AR_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAR, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAR = batchsh5_dir + 'step5.1_IDBA-UD_TID' + i + '_AR.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/idba-ud/' +  'AR_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/idba-ud/' + 'AR_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/idba-ud/' +  'AR_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

				shFileAB = batchsh4_dir + 'step4.1_IDBA-UD_TID' + i + '_AB.sh'
				assemblyFa = indir + '/idba-ud/' +  'AB_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/idba-ud/' +  'AB_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAB, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAB = batchsh5_dir + 'step5.1_IDBA-UD_TID' + i + '_AB.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/idba-ud/' +  'AB_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/idba-ud/' + 'AB_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/idba-ud/' +  'AB_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAB, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

				shFileAR = batchsh4_dir + 'step4.1_SUPERNOVA_TID' + i + '_AR.sh'
				assemblyFa = indir + '/supernova/' +  'AR_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/supernova/' +  'AR_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAR, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAR = batchsh5_dir + 'step5.1_SUPERNOVA_TID' + i + '_AR.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/supernova/' +  'AR_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/supernova/' + 'AR_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/supernova/' +  'AR_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

				shFileAB = batchsh4_dir + 'step4.1_SUPERNOVA_TID' + i + '_AB.sh'
				assemblyFa = indir + '/supernova/' +  'AB_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/supernova/' +  'AB_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAB, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAB = batchsh5_dir + 'step5.1_SUPERNOVA_TID' + i + '_AB.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/supernova/' +  'AB_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/supernova/' + 'AB_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/supernova/' +  'AB_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAB, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

			elif args.strategy == 'allread':
				shFileAR = batchsh4_dir + 'step4.1_IDBA-UD_TID' + i + '_AR.sh'
				assemblyFa = indir + '/idba-ud/' +  'AR_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/idba-ud/' +  'AR_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAR, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAR = batchsh5_dir + 'step5.1_IDBA-UD_TID' + i + '_AR.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/idba-ud/' +  'AR_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/idba-ud/' + 'AR_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/idba-ud/' +  'AR_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

				shFileAR = batchsh4_dir + 'step4.1_SUPERNOVA_TID' + i + '_AR.sh'
				assemblyFa = indir + '/supernova/' +  'AR_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/supernova/' +  'AR_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAR, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAR = batchsh5_dir + 'step5.1_SUPERNOVA_TID' + i + '_AR.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/supernova/' +  'AR_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/supernova/' + 'AR_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/supernova/' +  'AR_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)
			elif args.strategy == 'allbarcode':
				shFileAB = batchsh4_dir + 'step4.1_IDBA-UD_TID' + i + '_AB.sh'
				assemblyFa = indir + '/idba-ud/' +  'AB_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/idba-ud/' +  'AB_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAB, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAB = batchsh5_dir + 'step5.1_IDBA-UD_TID' + i + '_AB.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/idba-ud/' +  'AB_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/idba-ud/' + 'AB_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/idba-ud/' +  'AB_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)

				shFileAB = batchsh4_dir + 'step4.1_SUPERNOVA_TID' + i + '_AB.sh'
				assemblyFa = indir + '/supernova/' +  'AB_' + i + '/scaffold.fa'
				refGenomeFa =  refGenomeDir + '/' + i + '_genomic.fa'
				outdir = assessment_dir + '/supernova/' +  'AB_' + i
				mkdirIfNotExists(outdir)
				quast_bin_for_single_fasta(shFileAB, quastPY, assemblyFa, refGenomeFa, threads, outdir, IDY)

				shFileAB = batchsh5_dir + 'step5.1_SUPERNOVA_TID' + i + '_AB.sh'
				binFilterPY = dirname + '/script/bin_filter.py'
				assemblyFa = indir + '/supernova/' +  'AB_' + i + '/scaffold.fa'
				filteredFa = binfilter_dir + '/supernova/' + 'AB_' + i + '_filtered.fa'
				quastAlnTsv = assessment_dir + '/supernova/' +  'AB_' + i + '/contigs_reports/all_alignments_scaffold.tsv'
				create_binfilter_sh(shFileAR, binFilterPY, assemblyFa, filteredFa, refGenomeFa, quastAlnTsv, IDY, PCT)
			else:
				print('Please select valid reads strategy')

	else:
		print('No species depth reach the condition!!!')

### checkM bin result
checkm_stats_parameter = 'lineage_wf -t 20 -x fasta --nt --tab_table -f bins_qa.txt'
MetaWRAPsourch = '/zfsqd1/ST_OCEAN/USRS/st_ocean/MetaWRAP/source.sh'
def checkm_bin_for_single_fasta(shfile, MetaWRAPsource, check_parameter, intaxid_dir, outaxid_dir):
	checkm_stats_parameter = 'lineage_wf -t 20 -x fasta --nt --tab_table -f bins_qa.txt'
	checkm_plots_parameter = 'bin_qa_plot --image_type pdf -x fasta'
	command1 = ' '.join([ 'source', MetaWRAPsource ])
	command2 = ' '.join([ 'checkm', checkm_stats_parameter, intaxid_dir, outdir ])
	command3 = ' '.join([ 'checkm', checkm_plots_parameter, intaxid_dir, outdir ])
	command = '\n'.join([ command1, command2, command3 ])
	create_shell_script( 'CheckM_bin_fasta', shfile, command)

###########################################################################################################

shfile=commandsh_dir + 'step1.1.stlfr_split_barcode.sh'
rawfq1=args.fq1
rawfq2=args.fq2
barcode_list=dirname + '/source/barcode_list.txt'
split_barcodePL= dirname + '/script/split_barcode.pl'
sample=args.sample
outdir = cleandata_dir

if os.path.exists(outdir):
	pass
	stlfr_split_barcode_shell(shfile, split_barcodePL, barcode_list, rawfq1, rawfq2, sample, outdir)
else:
	os.mkdir(outdir)
	stlfr_split_barcode_shell(shfile, split_barcodePL, barcode_list, rawfq1, rawfq2, sample, outdir)

shfile=commandsh_dir + 'step1.2.stlfr_data_clean.sh'
barfq1='split_reads.1.fq.gz'
barfq2='split_reads.2.fq.gz'
soap_filter='/dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/xumengyang/software/stlfr2supernova_pipeline/bin/SOAPfilter_v2.2'
soap_parameter='-t 20 -y -F CTGTCTCTTATACACATCTTAGGAAGACAAGCACTGACGACATGA -R TCTGCTGAGTCGAGAACGTCTCTGTGAGCCAAGGAGTTGCTCTGG -p -M 2 -f -1 -Q 10'
sample=args.sample
outdir=cleandata_dir + '/cleandata/'
if os.path.exists(outdir):
	pass
	stlfr_data_clean_shell(shfile, barfq1, barfq2, soap_filter, soap_parameter, sample, outdir)
else:
	os.mkdir(outdir)
	stlfr_data_clean_shell(shfile, barfq1, barfq2, soap_filter, soap_parameter, sample, outdir)

shfile=commandsh_dir + 'step2.1.run_kraken.sh'
cleanfq1=cleandata_dir+'/cleandata/split_reads.1.fq.gz.clean.gz'
cleanfq2=cleandata_dir+'/cleandata/split_reads.2.fq.gz.clean.gz'
kraken='/zfsqd1/ST_OCEAN/USRS/zhangyue4/tools/kraken2/build/kraken2'
kraken_parameter='--threads '+ args.threads + ' --gzip-compressed --paired --db ' + args.kraken_db
sample=args.sample
outdir=taxonomy_dir+'/kraken/'
if os.path.exists(outdir):
	pass
	run_kraken_shell(shfile, cleanfq1, cleanfq2, kraken, kraken_parameter, sample, outdir)
else:
	os.mkdir(outdir)
	run_kraken_shell(shfile, cleanfq1, cleanfq2, kraken, kraken_parameter, sample, outdir)

shfile=commandsh_dir + 'step2.2.get_species_reads_and_abundance.sh'
splitterCC=dirname + '/script/SplitReads'
species_genome_size=args.genome_sz
kraken_C=taxonomy_dir+'/kraken/' + args.sample + '.C'
outdir=taxonomy_dir + '/SSRlist/'
mkdirIfNotExists(outdir)
min_depth, limited_depth = 10, 300
get_all_single_species_reads_list(shfile, splitterCC, species_genome_size, min_depth, limited_depth, kraken_C, outdir)

####
X10=[]
X300=[]

filelist = os.listdir(taxonomy_dir + '/SSRlist/')
for i in filelist:
	if i.startswith('10X'):
		taxid=i.split('.')[1].split('_')[1]
		X10.append(taxid)
	elif i.startswith('300X'):
		taxid=i.split('.')[1].split('_')[1]
		X300.append(taxid)
	else:
		pass
###
seqtk=dirname + '/tools/seqtk'
indir=taxonomy_dir + '/SSRlist/'
id2fq_dir=taxonomy_dir + '/id2fq/'
cleanfq1=cleandata_dir + '/cleandata/split_reads.1.fq.gz.clean.gz'
cleanfq2=cleandata_dir + '/cleandata/split_reads.2.fq.gz.clean.gz'

mkdirIfNotExists(id2fq_dir)
create_batch_fq_convert_sh(X10, X300, seqtk, indir, id2fq_dir, cleanfq1, cleanfq2)

###
indir=taxonomy_dir + '/id2fq/'
outdir=assembly_dir
fq2fa='/dellfsqd2/ST_OCEAN/biosoft/pipeline/meta_pipeline/Assembly/Assembly_idba/bin/idba/bin/fq2fa'
idba_ud='/dellfsqd2/ST_OCEAN/biosoft/pipeline/meta_pipeline/Assembly/Assembly_idba/bin/idba/bin/idba_ud'
idba_parameter='--mink 23 --maxk 83  --step 20 --num_threads 6 --pre_correction'

mkdirIfNotExists(outdir)
create_batch_idba_assembly_sh(X10, X300, indir, outdir, fq2fa, idba_ud, idba_parameter)

###
indir=taxonomy_dir + '/id2fq/'
outdir=assembly_dir
python2='/dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/zhangyue4/python/Python-2.7.10/bin/python2'
supernovaPY = dirname + '/script/supernova/clean_stlfr2supernova.py'
supernova_parameter='-f 0 -m 1 -supernova /dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/xumengyang/software/supernova4stLFR/ \
-s /dellfsqd1/ST_OCEAN/ST_OCEAN/USRS/xumengyang/software/stlfr2supernova_pipeline/clean_stLFR_data2supernova/ '

mkdirIfNotExists(outdir)
create_batch_supernova_assembly_sh(X10, X300, python2, indir, outdir, supernovaPY, supernova_parameter)

indir = assembly_dir
refGenomeDir = args.kraken_fa
threads = 16
quastPY = dirname + '/tools/quast.py'
IDY = args.IDY
PCT = args.PCT
assessment_dir = filefold + '/step4_assessment/'
mkdirIfNotExists(assessment_dir)
binfilter_dir = filefold + '/step5_binfilter/'
mkdirIfNotExists(binfilter_dir)
create_batch_quast_binfilter_sh(X10, X300, refGenomeDir, indir, assessment_dir, binfilter_dir, threads, quastPY, IDY, PCT)