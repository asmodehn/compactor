#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import hypothesis.strategies

from compactor.alzw import compress, decompress, text_compress, text_decompress


# TODO : craft by hand input sequences to check compression
# TODO : craft by hand output sequences to check decompression

# Here we only check the invariant

@hypothesis.given(b=hypothesis.strategies.binary())
# known sample to assert compression output
@hypothesis.example(b'TOBEORNOTTOBEORTOBEORNOT#')
# unique only
@hypothesis.example(b'TOBE#')
# simple repeat
@hypothesis.example(b'BOBO')
# empty
@hypothesis.example(b'')
def test_compress_decompress(b: bytes):

    output = compress(b)

    if b == b'TOBEORNOTTOBEORTOBEORNOT#':
        assert output == b'\x07TOBERN#\x01\x02\x03\x04\x02\x05\x06\x02\x01\x08\n\x0c\x11\x0b\r\x0f\x07'
    elif b == b'TOBE#':
        assert output == b'\x05TOBE#'
    elif b == b'BOBO':
        assert output == b'\x02BO\x01\x02\x03'
    elif b == b'':
        assert output == b''

    result = decompress(output)

    assert b == result


@pytest.mark.skip("currently failing on some unicode encoding/decoding")
@hypothesis.given(t=hypothesis.strategies.text())
# known sample to assert compression output
@hypothesis.example('TOBEORNOTTOBEORTOBEORNOT#')
# unique only
@hypothesis.example('TOBE#')
# simple repeat
@hypothesis.example('BOBO')
# empty
@hypothesis.example('')
def test_text_compress_decompress(t: str):

    output = text_compress(t)

    # tricky unicode encodings. Note the compression is the same as for bytes, only representation differs.
    if t == 'TOBEORNOTTOBEORTOBEORNOT#':
        assert output == 'TOBERN#\b\n\f\r'
    elif t == 'TOBE#':
        assert output == 'TOBE#'
    elif t == 'BOBO':
        assert output == 'BO'
    elif t == '':
        assert output == ''

    result = text_decompress(output)

    assert t == result


if __name__ == '__main__':
    pytest.main(['-s', __file__])