#!/bin/bash
# Grid search over `k` and `b` for Okapi BM25 algorithm on the ClueWeb12 Disk B corpus using topics from TREC 2013 and 2014 Web Track.
# Performs evaluation using `trec_eval` and `gdeval.pl`

# Path to the anserini folder.
anseriniPath='anserini'
# Path to the clueweb 12 Disk b index.
cluewebPath='/ir/index/lucene-index.cw12b13.pos+docvectors+transformed'

for k in $(seq 0.1 0.1 2.0); do 
	for b in $(seq 0.0 0.2 1.0); do
		$anseriniPath/target/appassembler/bin/SearchCollection -topicreader Webxml -index $cluewebPath -topics $anseriniPath/src/main/resources/topics-and-qrels/topics.web.201-250.txt -output results/bm25var/k"$k"_b"$b"_201-250.txt -bm25 -k1 $k -b $b
		$anseriniPath/target/appassembler/bin/SearchCollection -topicreader Webxml -index $cluewebPath -topics $anseriniPath/src/main/resources/topics-and-qrels/topics.web.251-300.txt -output results/bm25var/k"$k"_b"$b"_251-300.txt -bm25 -k1 $k -b $b
	done
done

for filename in results/bm25var/*.txt; do
	[ -e "$filename" ] || continue
	base=${filename##*/}
	name=${base:0:9}
	nums=${base:10:7}
	$anseriniPath/eval/gdeval.pl $anseriniPath/src/main/resources/topics-and-qrels/qrels.web."$nums".txt $filename >> results/bm25var/output/res_"$name"_"$nums".txt
	$anseriniPath/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 $anseriniPath/src/main/resources/topics-and-qrels/qrels.web."$nums".txt $filename >> results/bm25var/output/res_"$name"_"$nums".txt
done
