





# step 1 #################################################################################################
def stlfr_split_barcode_shell(shfile, split_barcodePL, barcode_list, rawfq1, rawfq2, sample, outdir):
	command1 = 'cd ' + outdir
	command2 = ' '.join(['perl', split_barcodePL, barcode_list, rawfq1, rawfq2, 'split_reads'  ])
	command = '\n'.join([command1, command2])
	create_shell_script( 'step1.1 stlfr_split_barcode', shfile, command)

