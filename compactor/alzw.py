from typing import Dict
from .iterutils import unique_everseen

"""
Alphabetized LZW
Compression similar to LZW algorithm, but we alo include the alphabet ( list of symbols )
in the compressed output. Works best for alphabets << 256 and long data sequence
"""


# TODO : investigate memory view for faster perfs
def compress(data: bytes) -> bytes:
    """
    Lempel Ziv Welch Encoding
    References :
    https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
    https://www.geeksforgeeks.org/lzw-lempel-ziv-welch-compression-technique/
    http://rosettacode.org/wiki/LZW_compression#Python
    :param data:
    :return:
    """

    # First we visit the data once to collect all symbols, and their corresponding int
    keys: Dict[bytes, int] = {d.to_bytes(1, byteorder='big'): counter for counter, d in enumerate(unique_everseen(data), 1)}
    # store the number of initial keys for later
    n_init_keys: int = len(keys)

    # Special Case : if the data is only unique symbols (or empty), we don't need to even attempt compression
    if n_init_keys == len(data):
        return bytes([n_init_keys]) + data if n_init_keys else b''

    #: the compressed list of encoded sequences
    compressed: list = []
    #: the current sequence being checked for possible compression
    seq: bytearray = bytearray()
    # looping only once on the data
    for idx in range(len(data)):
        #: the next character being considered
        nextc = data[idx]
        #: the next bytes sequence
        nextseq = bytes(seq + data[idx].to_bytes(1, byteorder='big'))

        # if the sequence and the next char are in the keys
        if nextseq in keys:
            # we append into seq, and we will check the new sequence in next loop
            seq.append(nextc)
        else:
            # we stop here, output the encoding for the sequence we had until here
            compressed.append(keys[bytes(seq)])
            # and add the new sequence to the dictionary ( in case we encounter it later )
            keys[nextseq] = len(keys)+1
            # the new sequence to check starts from here
            seq = bytearray([nextc])

    code = keys.get(bytes(seq))
    # handling case when input is empty -> no keys available
    if code:
        # final sequence ( we are sure at this point that it is in keys )
        compressed.append(code)

        # to that we need to prepend our initial alphabet, as well as its size (always <256 since we take initial alphabet byte by byte)
        output = [n_init_keys] + [int.from_bytes(k, byteorder='big') for c, k in enumerate(keys, 0) if c < n_init_keys] + compressed

    else:  # no keys means no input
        output = []

    # Finally we need to generate our output byte sequence
    return bytes(output)


def text_compress(data: str) -> str:
    encoded: bytes = data.encode()
    compressed: bytes = compress(encoded)
    decoded: str = compressed.decode('utf-8', errors='backslashreplace')
    return decoded


def decompress(data: bytes) -> bytes:
    # recover the initial alphabet from the data
    # and find the beginning of the compressed data
    keys: Dict[int, bytes] = dict()
    n_init_keys = data[0] if data else 0
    if n_init_keys:
        compressed: bytes = data[1+data[0]:]
    else:  # no input, no output
        return b''

    if not compressed:
        # if there is no compressed subsequence, it means the original sequence was the alphabet (only uniques)
        return data[1:]

    for idx in range(1, n_init_keys+1):
        # populate the dictionary (reverse pair compared to compression dict)
        keys[idx] = data[idx].to_bytes(1, byteorder='big')

    decompressed = bytearray()
    # we always have a compressed list here
    previous = keys[compressed[0]]
    decompressed += previous

    for d in compressed[1:]:
        current: bytes = b''
        try:
            # retrieve the bytes sequence in dictionary
            current = keys[d]
        except KeyError:
            # if it fails
            if d == len(keys)+1:  # and our code is just the size of the dict
                # we compute the sequence
                current = previous + previous[:1]
            else:
                raise ValueError(f"ERROR decompressing {d} with {keys}")
        finally:
            decompressed += current
            # we create the symbol for the code we just encountered and store it for the next time we encounter it
            keys[len(keys)+1] = previous + current[:1]
            previous = current

    return bytes(decompressed)


def text_decompress(data: str) -> str:
    encoded: bytes = data.encode()
    decompressed: bytes = decompress(encoded)
    decoded: str = decompressed.decode('utf-8', errors='backslashreplace')
    return decoded
