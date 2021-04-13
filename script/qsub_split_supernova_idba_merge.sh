outdir=$1
cd $outdir/step0_commandsh/step2.4.convert_single_species_fq_sh;
mkdir -p $outdir/step0_commandsh/step4.0.merge_idba_supernova_sh
ls step2.4*.sh |while read line;
do
	depth=`echo $line|cut -d'_' -f 2`;
	tid=`echo $line|cut -d'_' -f 3`;
	strategy=`echo $line|cut -d'_' -f 4`;
	if [ $depth == 'X10' ];
		then
		record=`qsub -cwd -l vf=10g,num_proc=1 -P P18Z19700N0076 -q st.q -binding linear:1 $line`;
		qid=`echo $record|awk '{print $3}'`;
		echo sh $outdir/step0_commandsh/step3.1.batch_supernova_assembly_sh/step3.1_X10_$tid\_$strategy '&&' sh $outdir/step0_commandsh/step3.2.batch_idba_assembly_sh/step3.2_X10_$tid\_$strategy > $outdir/step0_commandsh/step4.0.merge_idba_supernova_sh/step4.0_X10_$tid\_$strategy;
		qsub -cwd -hold_jid $qid -l vf=40g,num_proc=16 -P P18Z19700N0076 -q st.q -binding linear:16 $outdir/step0_commandsh/step4.0.merge_idba_supernova_sh/step4.0_X10_$tid\_$strategy
	elif [ $depth == 'X300' ];
		then
		record=`qsub -cwd -l vf=30g,num_proc=1 -P P18Z19700N0076 -q st.q -binding linear:1 $line` ;
		qid=`echo $record|awk '{print $3}'`;
		qsub -cwd -hold_jid $qid -l vf=90g,num_proc=16 -P P18Z19700N0076 -q st.q -binding linear:16 $outdir/step0_commandsh/step3.1.batch_supernova_assembly_sh/step3.1_X300_$tid\_$strategy;
		qsub -cwd -hold_jid $qid -l vf=50g,num_proc=16 -P P18Z19700N0076 -q st.q -binding linear:16 $outdir/step0_commandsh/step3.2.batch_idba_assembly_sh/step3.2_X300_$tid\_$strategy;
	else
		echo 'Print Error' $line
	fi
done
