#!/bin/bash
# Grid search over `fbt`, `fbd` and `w` for the BM25PRF algorithm on the ClueWeb12 Disk B corpus using topics from TREC 2013 and 2014 Web Track.
# Performs evaluation using `trec_eval` and `gdeval.pl`

# Path to the anserini folder.
anseriniPath='anserini'
# Path to the clueweb 12 Disk b index.
cluewebPath='/ir/index/lucene-index.cw12b13.pos+docvectors+transformed'

for qnum in 201 251; do
	for fbt in 1 5 10 15; do
		for fbd in 1 5 10 15; do
			for w in 0.1 0.2 0.5 0.7 1; do
				lastqnum=$(($qnum + 49))
				$anseriniPath/target/appassembler/bin/SearchCollection -topicreader Webxml -index $cluewebPath -topics $anseriniPath/src/main/resources/topics-and-qrels/topics.web."$qnum"-"$lastqnum".txt -output results/bm25prf/k1.2_b0.3_fbt"$fbt"_fbd"$fbd"_w"$w"_"$qnum"-"$lastqnum".txt -bm25 -k1 1.2 -b 0.3 -bm25prf -bm25prf.fbTerms "$fbt" -bm25prf.fbDocs "$fbd" -bm25prf.newTermWeight "$w" -bm25prf.k1 1.2 -bm25prf.b 0.3
			done
		done
	done
done

for filename in results/bm25prf/*.txt; do
	[ -e "$filename" ] || continue
	base=${filename##*/}
	name=${base:0: -12}
	nums=${base: -11:-4}
	$anseriniPath/eval/gdeval.pl $anseriniPath/src/main/resources/topics-and-qrels/qrels.web."$nums".txt $filename >> results/bm25prf/output/res_"$name"_"$nums".txt
	$anseriniPath/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 $anseriniPath/src/main/resources/topics-and-qrels/qrels.web."$nums".txt $filename >> results/bm25prf/output/res_"$name"_"$nums".txt
done
