#!/bin/bash

# 1) remover caracteres indesejados e formatacoes da wikipedia
# real	45m12.346s
# user	38m4.767s
# sys	1m6.775s

# time perl preprocessing.pl /scratch2/evelin.amorim/enwiki-latest-pages-articles.xml > /scratch2/evelin.amorim/wiki_clean.txt

# 2) dividir em sentencas a wiki limpa
# real    142m45.142s
# user    136m32.194s
# sys     1m36.135s
echo "dividir em sentencas a wiki limpa"
time python3 preprocessing.py /scratch2/evelin.amorim/wiki_clean.txt -ps 

# 3) ordena o arquivo de sentencas
# real    36m31.528s
# user    41m32.681s
# sys     1m15.747s
echo "ordena o arquivo de sentencas"
time sort /scratch2/evelin.amorim/wiki_sentences.txt > /scratch2/evelin.amorim/wiki_sorted.txt
# time sort wiki_sentences.txt > wiki_sorted.txt

# 4) remove duplicate sentences
# real    606m41.605s
# user    604m11.434s
# sys     1m36.455s
echo "remove duplicate sentences"
time python3 preprocessing.py /scratch2/evelin.amorim/wiki_clean.txt -nps -rd

# 5) treinar
time ./word2vec -train /scratch2/wiki_sentences_nodup.txt -output vectors.bin -cbow 1 -size 600 -window 5 -negative 15 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15 -min-count 100 ./distance vectors_wikien.bin
