import corpusbuilder
import itertools
import ahocorasick
from numba import njit, objmode, prange, types,int32
import time
#@njit(types.containers.List(dtype=types.unicode_type)(types.containers.List(dtype=types.unicode_type)),cache=True)
def pair_maker(input_list):
  base = len(input_list)
  result = ["" for _ in range(0)]
  for i in prange(base**2):
    first_count,last_count = divmod(i,base)
    first_count,last_count = int(first_count),int(last_count)
    result.append(input_list[first_count]+input_list[last_count])
    if first_count != last_count:
      result.append(input_list[last_count]+input_list[first_count])
    result = sorted(result)
  return result
#@njit(types.containers.List(dtype=types.unicode_type)(types.unicode_type,int32),cache=True,nogil=True,parallel=True)
def generate_token_list(corpus:str,size=1024):
  token_list = list(set(corpus))
  combination_list = pair_maker(token_list)
  num_pairs = len(combination_list)
  pairs_freq = dict()
  exclusion_pairs = []
  while len(token_list) < size:
    print(len(token_list))
    combination_list = pair_maker(token_list)
    num_pairs = len(combination_list)
    start = time.time()
    for i in prange(0,num_pairs):
      pair = combination_list[i]
      if pair in exclusion_pairs:
        continue
      if (pair not in pairs_freq):
        frequency = corpus.count(pair)
        pairs_freq[pair] = frequency
    print(time.time()-start)
    max_frequency = max(pairs_freq.values())
    if max_frequency < 2:
      print("Frequency's too low")
      print(max(pairs_freq.values()))
      break
    else:
      for k, v in pairs_freq.items():
        if v == max_frequency:
          new_token = k
          break
      token_list.append(new_token)
      exclusion_pairs.append(new_token)
      pairs_freq.pop(new_token)
  return token_list
full_corpus = corpusbuilder.build("./OANC/data/**/*.txt")
token_list = generate_token_list(full_corpus,size=1024)
print(token_list)