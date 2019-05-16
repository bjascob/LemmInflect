To get the raw BWCorpus data do..
  wget http://statmt.org/wmt11/training-monolingual.tgz
  tar --extract -v --file training-monolingual.tgz --wildcards training-monolingual/news.20??.en.shuffled
  This gives the raw unprocessed, text
