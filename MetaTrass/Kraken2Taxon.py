






def run_kraken_shell(shfile, cleanfq1, cleanfq2, kraken, kraken_parameter, sample, outdir):
	command = ' '.join([ kraken,  kraken_parameter,  '--report', outdir+sample+'.R', '--output', outdir+sample+'.C', cleanfq1, cleanfq2 ])
	create_shell_script('step2.1 run_kraken', shfile, command)