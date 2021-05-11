from helpfuncs import bitdecoding
from glob import globs

N = globs["size"]

# initialize and fill list for set based on base relations
bsplit = [(len(bitdecoding(i+1)),bitdecoding(i+1)) for i in range((2**N)-1)]


