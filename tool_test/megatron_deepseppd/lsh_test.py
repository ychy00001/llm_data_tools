from lsh import cache, minhash
import numpy as np
import time

# lsh install https://github.com/mattilyra/LSH

# set seed and get an array of seeds of 100 integers
np.random.seed(1234)
seeds = np.random.randint(0, 1e6, size=100)

# initialize minhash and lsh cache
hasher = minhash.MinHasher(seeds=seeds, char_ngram=5, hashbytes=4)
lshcache = cache.Cache(num_bands=20, hasher=hasher)


def compute_fingerprint(line):
    try:
        fingerprint = hasher.fingerprint(line)
    except Exception as e:
        print('Error:', e)
        return None, False

    return fingerprint, True


# This function is adapted from:
#   https://github.com/mattilyra/LSH/blob/master/examples/Introduction.ipynb
def shingles(text, char_ngram=5):
    return set(text[head:head + char_ngram]
               for head in range(0, len(text) - char_ngram))


# This function is adapted from:
#  https://github.com/mattilyra/LSH/blob/master/examples/Introduction.ipynb
def jaccard(set_a, set_b):
    if len(set_a) < 1 or len(set_b) < 1:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def url_pairs_to_remove(bucket_lines):
    remove_lines_list = []
    deduped_local, counter_local = 0, 0
    iteration = 0
    while len(bucket_lines) > 1:
        items = list(bucket_lines)
        remove_lines = []
        main_line = items[np.random.randint(0, len(items))]
        main_dhingles = shingles(main_line)

        for i in range(0, len(items)):
            counter_local += 1
            other_line = items[i]
            if other_line == main_line:
                continue
            other_shingles = shingles(other_line)
            try:
                jaccard_sim = jaccard(main_dhingles, other_shingles)
            except Exception as e:
                print('Error:', e)
                jaccard_sim = 0.0
            if jaccard_sim > 0.5:
                remove_lines.append({other_line: jaccard_sim})
                deduped_local += 1
                bucket_lines.remove(other_line)

        bucket_lines.remove(main_line)
        if len(remove_lines) > 0:
            remove_lines_list.append({main_line: remove_lines})
        iteration += 1
    return remove_lines_list, deduped_local, counter_local


def write_remove_lines_list(remove_lines_list):
    if len(remove_lines_list) > 0:
        for each_url_remove in remove_lines_list:
            print(f"移除重复行：{each_url_remove}")


if __name__ == '__main__':
    with open("./test_data.txt", "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            fingerprint, _ = compute_fingerprint(line)
            lshcache.add_fingerprint(fingerprint, line)
    print(f"读取行数：{len(lines)}")
    start_time = time.time()
    deduped, counter = 0, 0
    for b in lshcache.bins:
        for bucket_id in b:
            bucket_line = b[bucket_id].copy()
            if len(b[bucket_id]) <= 1:
                continue
            bucket_lines = b[bucket_id].copy()
            remove_lines_list_sub, deduped_local_sub, counter_local_sub = \
                url_pairs_to_remove(bucket_lines)

            deduped += deduped_local_sub
            counter += counter_local_sub
            write_remove_lines_list(remove_lines_list_sub)
            # print(' [write]> processed {} documents in {:.2f} '
            #       'seoncds and deduped {} documents ...'.format(counter, time.time() \
            #                                                     - start_time, deduped), flush=True)
    # print(' [write]> processed {} documents in {:.2f} '
    #       'seoncds and deduped {} documents ...'.
    #       format(counter, time.time() - start_time,
    #              deduped), flush=True)
