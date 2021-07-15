



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