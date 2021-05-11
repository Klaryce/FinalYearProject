from helpfuncs import bitdecoding
from glob import globs

N = globs["size"]

# initialize and fill list for set based on base relations
# bitdecoding 根据数字返回base relations. bsplit返回2的N次方范围内每个数字对应的关系
bsplit = [(len(bitdecoding(i+1)),bitdecoding(i+1)) for i in range((2**N)-1)]


