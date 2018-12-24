import io
import pytest
import hypothesis.strategies

from compactor.streams import stream_compress, stream_decompress, stream_noop


@hypothesis.given(b=hypothesis.strategies.binary())
def test_stream_noop(b: bytes):
    """
    Testing the stream interface, no compaction
    """
    bufb = io.BufferedReader(io.BytesIO(b))

    # to store our output
    c = io.BytesIO()
    bufc = io.BufferedWriter(c)

    orig_size, nooped_size = stream_noop(bufb, bufc)

    assert orig_size == nooped_size
    assert c.getvalue() == b


@pytest.mark.skip(reason="Implementation still buggy.")
@hypothesis.given(b=hypothesis.strategies.binary())
# known sample to assert compression output
@hypothesis.example(b'TOBEORNOTTOBEORTOBEORNOT#')
# unique only
@hypothesis.example(b'TOBE#')
# empty
@hypothesis.example(b'')
def test_stream_compress_uncompress(b: bytes):
    """
    Testing the stream interface, no compaction
    """
    bufb = io.BufferedReader(io.BytesIO(b))

    # to store our output
    c = io.BytesIO()
    bufc = io.BufferedRWPair(c, c)  # since we write and read at different times this should be fine

    orig_size, compressed_size = stream_compress(bufb, bufc)

    if b == b'TOBEORNOTTOBEORTOBEORNOT#':
        assert c.getvalue() == b'\x00\x19\x00\x19\x07TOBERN#\x01\x02\x03\x04\x02\x05\x06\x02\x01\x08\n\x0c\x11\x0b\r\x0f\x07'
    elif b == b'TOBE#':
        assert c.getvalue() == b'\x05TOBE#'
    elif b == b'':
        assert c.getvalue() == b''

    d = io.BytesIO()
    bufd = io.BufferedWriter(d)

    orig_compressed_size, uncompressed_size = stream_decompress(bufc, bufd)

    assert compressed_size == orig_compressed_size
    assert orig_size == uncompressed_size
    assert d.getvalue() == b


# TODO : test random access performance after compaction


if __name__ == '__main__':
    pytest.main(['-s', __file__])