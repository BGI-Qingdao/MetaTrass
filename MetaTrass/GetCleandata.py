




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
