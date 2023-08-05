python-neoscrypt-wrapper
========================

* src/          || neoscrypt source files (C)
* scripts/      || ie. cross-compiling scripts to create .so, .dylib or dll
* tests/        || python neoscrypt testfile

This Software needs compile (gcc, mingw ...)

Install from git
----------------

Compiling and installing as PythonModule (python2/python3)::

    bash:~/: sudo python3 -m pip install git+https://github.com/sparkspay/python-neoscrypt.git
     
    or
     
    bash:~/: git clone git+https://github.com/sparkspay/python-neoscrypt.git
    bash:~/: cd python-neoscrypt
    bash:~/: python-neoscrypt/: sudo python3 setup.py install



Pypi Version install will be available ::

    bash:~/: pip install neoscrypt


NeoScrypt
=========

NeoScrypt is a strong memory intensive key derivation function.

* Compile time definitions: --DNEOSCRYPT_SHA256 enables optional SHA-256
* support (Scrypt compatibility); --DNEOSCRYPT_BLAKE256 enables optional
* BLAKE-256 support; --DNEOSCRYPT_OPT enables FastKDF performance
* optimisations; --DNEOSCRYPT_ASM enables 32-bit and 64-bit assembly
* optimisations; --DNEOSCRYPT_MINER_4WAY enables 4-way mining per thread (requires -DNEOSCRYPT_ASM).


Documentation
-------------

Refer to the following white paper for an introduction to NeoScrypt:
http://phoenixcoin.org/archive/neoscrypt_v1.pdf

Source Links
============

https://github.com/goacoincore/neoscrypt -> goacoincore

https://github.com/ghostlander/NeoScrypt -> ghostlander