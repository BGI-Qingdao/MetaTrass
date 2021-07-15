


def supernova_assembly_shell(shfile, python2, supernovaPY, supernova_parameter, tssfq1, tssfq2, sample, outdir):
	supernova_dir = outdir + '/supernova/' + sample
	command1 = ' '.join([ 'mkdir -p ', supernova_dir, ' && cd ', supernova_dir ])
	command2 = ' '.join([ python2, supernovaPY, supernova_parameter, '-n', sample, '-r1', tssfq1, '-r2', tssfq2,'-o', supernova_dir ])
	command3 = ' '.join([ 'mv', supernova_dir + '/supernova_out/supernova_out.mri.tgz', supernova_dir ])
	command4 = ' '.join([ 'rm -rf', supernova_dir + '/supernova_out/' ])
	command5 = ' '.join([ 'gunzip -c', supernova_dir+'/'+sample+'_supernova_result.fasta.gz', '>', supernova_dir + '/scaffold.fa'])
	command6 = ' '.join([ 'rm -rf', supernova_dir + '/*.fastq.gz'])
	command = '\n'.join([ command1, command2, command3, command4, command5, command6 ])
	create_shell_script( 'supernova_assembly_shell', shfile, command)


