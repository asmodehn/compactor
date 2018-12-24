Compactor
=========

Python package providing a custom LZW-like encoding, with alphabet.

Python 3.7 required

How to use
==========

Get latest python at https://www.python.org/getit/
Note using pyenv https://github.com/pyenv/pyenv is an easy way to do that on linux systems

And then, in your new python environment
```
pip install pipenv
pipenv install
pipenv run mypy compactor
pipenv run pytest tests
```

To use on a string(for testing purposes).
Disclaimer : Depending on unicode support on your machine, trying to decompress the outputted string may not work.
```
echo "mystring" | pipenv run python -m compacter
```

To use on a file:
```
pipenv run python -m compacter -f <myfile>
```

Design Consideration
====================

We aim at providing a package(currently not installable) containing various compression algorithms.
We will keep simple interfaces (bytes, bufferedStream, commandline and stdin/stdout) to be able to "plug" compression in a wide variety of settings.

There may eventually be many more or less complex compression algorithms.
Currently there is only one custom one available.

Known issues : Stream API is currently buggy.

Roadmap
=======
- [X] First custom algorithm and tests with bytes interface
- [/] support unicode string encoding/decoding
- [/] Stream interface to connect with any buffered IO
- [ ] Tests Coverage
- [ ] Integration tests for CLI & stdin/stdout interface
- [ ] Continuous Integration (Travis)
- [ ] Standard compression algorithms (Zip, etc.)
- [ ] setup.py for use to install it ( with convenient entry points )
- [ ] provide optional extra to allow user to test on their own machine
- [ ] embedded performance checks
- [ ] provide a simple process (that can be easily hooked into twisted or others framework) that self optimise on stream chunk size during long runs.


Compression Details
===================

Alphabet LZW
------------

Custom algorithm, following a LZW compression with additional alphabet embedding ( useful for small alphabet ).
To known the alphabet, we have to do two passes, chunk by chunk, which means each chunk will be compressed with different alphabets.
Chunks are indexed in compressed space for uncompression and in original space for random access (not implemented).

Possible Improvements::

- Increased compacting would be possible by reducing the byte representation of a character to not more than the few bits needed for all possible characters.
- Further optimization can be achieved if cache hierarchy structure and sizes are known, to help refine the maximal chunk size and avoid cache misses. This might even be doable dynamically, on a long running compression server.
