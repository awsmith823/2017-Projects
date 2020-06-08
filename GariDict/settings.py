
# directories
DIR_IMAGES = 'images'
DIR_SCHEMA = 'schema'
DIR_DATA = 'data'
# files
BATCH_FNAME = 'batch_images.txt'
DATA_FNAME_SEP_TUP = ('data.tsv', "\t")
# languages (ordered)
LANG_LIST = ["English", "Garifuna", "Spanish"]

# search params
PREFIX = 3
EDIT_DIST = 1
K_LIMIT = 5

search_params = {
    "prefix": PREFIX,
    "limit": K_LIMIT,
    "maxdist": EDIT_DIST,
    "languages": LANG_LIST,
}
