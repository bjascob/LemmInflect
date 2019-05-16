Use either Gutenberg or BWCorpus.  Only one overrides file is creates so choose which corpus to use.

Gutenberg is what's inside of NLTK so you don't need to download anything to use it but most texts
are more than 100 years old so there's a lot of older word forms.

To get the raw BWCorpus data do..
  wget http://statmt.org/wmt11/training-monolingual.tgz
  tar --extract -v --file training-monolingual.tgz --wildcards training-monolingual/news.20??.en.shuffled
  This gives the raw unprocessed, text
