import os

# Directory for temporary files used to build project files
data_repo = os.path.join(os.path.dirname(__file__), '..', 'data_repo')
data_repo = os.path.realpath(data_repo) # will resolve sym-links

# Directory for project files requried at run-time
proj_resources = os.path.join(os.path.dirname(__file__), '..', 'lemminflect', 'resources')
proj_resources = os.path.abspath(proj_resources)

# Corpuses used for building unigrams
gutenberg_dir  = '/mnt/raid/Data/Corpus/Gutenberg/Corpus_UMichVersion_3036Books'
bwcorp_dir     = '/home/bjascob/DataRepoTemp/BWCorpus/training-monolingual'

# Temporary files used in building the lexicon
unigrams_gb_all_fn   = os.path.join(data_repo, 'unigrams_gb_all.csv')
unigrams_gb_clean_fn = os.path.join(data_repo, 'unigrams_gb_clean.csv')
unigrams_bw_all_fn   = os.path.join(data_repo, 'unigrams_bw_all.csv')
unigrams_bw_clean_fn = os.path.join(data_repo, 'unigrams_bw_clean.csv')
unigrams_fn          = os.path.join(data_repo, 'unigrams.csv')
english_dict_fn      = os.path.join(data_repo, 'english_dict.txt')
lexicon_fn           = os.path.join(data_repo, 'LEXICON')
ftable_fn            = os.path.join(data_repo, 'forms_table.dat.gz')

# Project files used for lookup at run-time
lemma_lu_fn         = os.path.join(proj_resources, 'lemma_lu.csv.gz')
inflection_lu_fn    = os.path.join(proj_resources, 'infl_lu.csv.gz')

# Temporary files used with the NN models
model_lemma_cl_fn   = os.path.join(data_repo, 'model_lemma_classes.csv')
lemma_tcorp_fn      = os.path.join(data_repo, 'lemma_tcorp.csv.gz')
infl_tcorp_fn       = os.path.join(data_repo, 'infl_tcorp.csv.gz')

# Project locations for trained models
model_lemma_fn      = os.path.join(proj_resources, 'model_lemma.pkl.gz')
model_infl_fn       = os.path.join(proj_resources, 'model_infl.pkl.gz')

# Project overrides file locations
lemma_overrides_fn  = os.path.join(proj_resources, 'lemma_overrides.csv')
infl_overrides_fn   = os.path.join(proj_resources, 'infl_overrides.csv')

# default Keras model inference engine
kinfer_type         = 'numpy'   # numpy or keras
