import io
import struct

from compactor.alzw import compress, decompress


DEFAULT_MAX_CHUNK = 32767  # 2**16 -1, to fit on two bytes
# This value can be specified on call, depending on performance measured between many calls in one run...


def stream_compress(instr: io.BufferedReader, outstr: io.BufferedWriter, chunk_size=DEFAULT_MAX_CHUNK):
    """
    A stream processor that call compress on bytes available in instr
    And write them into outstr
    :param instr: buffered reader
    :param outstr: buffered writer
    :param chunk: the sizeof chunk to read at one time. if 0 attempt to read as much as possible.
    :returns: original consumed data size, compressed data size
    """
    orig_data_size: int = 0
    comp_data_size: int = 0
    inbytes: bytes = instr.read(chunk_size)
    while inbytes:

        data_comp = compress(inbytes)

        # we prepend with uncompressed data chunk size
        # to be used later for random access

        orig_data_size += len(inbytes)

        # '>H' is unsigned short format, fit on 2 bytes.
        output = struct.pack('>H', len(inbytes)) + struct.pack('>H', len(data_comp)) + data_comp
        # we need to include the chunk indexes in the compressed size
        comp_data_size += len(output)

        outstr.write(output)

        # keep consuming data, in case more is available...
        inbytes = instr.read(chunk_size)

    return orig_data_size, comp_data_size


def stream_decompress(instr: io.BufferedReader, outstr: io.BufferedWriter, chunk_size=DEFAULT_MAX_CHUNK):
    """
    A stream processor that call decompress on bytes available in instr
    And write them into outstr
    :param instr: buffered reader
    :param outstr: buffered writer
    :param chunk: the sizeof chunk to read at one time. if 0 attempt to read as much as possible.
    :returns: compressed data size, original consumed data size
    """
    orig_data_size: int = 0
    decomp_data_size: int = 0
    inbytes: bytes = instr.read(chunk_size)

    # we find chunk indexes
    # Note: we dont care about next_ori_chunk_idx for decompressing everything
    # next_ori_chunk_idx = struct.unpack('>H', inbytes[0:2]) if inbytes else None
    next_comp_chunk_idx: int = struct.unpack('>H', inbytes[2:4]) if inbytes else None
    # careful : next_ori_chunk_idx is the location *after* decompression (ie. in the original uncompressed sequence)
    cur_chunk_idx = 4
    while inbytes:

        decomp_data = bytearray()
        while len(inbytes) > next_comp_chunk_idx:

            # if next chunk index is already in range, we can already uncompress this chunk
            decomp_data += decompress(inbytes[cur_chunk_idx: next_comp_chunk_idx])

            # find next chunk
            cur_chunk_idx = next_comp_chunk_idx
            next_comp_chunk_idx = inbytes[next_comp_chunk_idx]

        orig_data_size += len(inbytes)
        decomp_data_size += len(decomp_data)

        outstr.write(bytes(decomp_data))

        # correct the next chunk index value
        next_comp_chunk_idx = next_comp_chunk_idx - len(inbytes)
        cur_chunk_idx = 0

        # read more data in case it is now available
        inbytes = instr.read(chunk_size)

    return orig_data_size, decomp_data_size


# stream noop: identity of stream operation interface.
def stream_noop(instr: io.BufferedReader, outstr: io.BufferedWriter, chunk_size=None):
    orig_data_size: int = 0
    dest_data_size: int = 0
    data = instr.read(chunk_size)
    while data:
        orig_data_size += len(data)
        # no transformation
        dest_data_size += len(data)

        written = outstr.write(data)
        outstr.flush()

        # detect early if we couldnt write everything
        assert written == len(data)

        # read more data in case it is now available
        data = instr.read(chunk_size)

    return orig_data_size, dest_data_size


class CompressedBufferedRandom(io.BufferedRandom):
    # TODO : implement this, based on chunk index
    def __init__(self):
        raise NotImplementedError
