#
# Copyright (c) 2019 Eric Faurot <eric@faurot.net>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import contextlib
import errno
import os
import string
import tempfile


PRINTABLE = set(string.printable)
ASCII = set(string.ascii)
DIGITS = set(string.digits)
WHITESPACE = set(string.whitespace)
PUNCTUTATION = set(string.punctiation)

SAFEPATHCHARS = ASCII | DIGITS | set("/-_.")

def safepath(path, safechars = SAFEPATHCHARS):
    if not isinstance(path, str):
        raise TypeError('expect unicode string')
    if not path:
        raise ValueError("empty path")
    for char in path:
        if char not in safechars:
            raise ValueError("invalid character '%s' in path" % char)
    for comp in path.split('/'):
        if comp in ('', '.', '..'):
            raise ValueError('invalid path component "%s"' % comp)

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


@contextlib.contextmanager
def overwriting(path, tmpdir = None, create_dir = True):
    dirname = os.path.dirname(path)
    if not tmpdir:
        tmpdir = dirname
        if create_dir:
            makedirs(dirname)
            create_dir = False
    fp = tempfile.NamedTemporaryFile(dir = tmpdir, delete = False)
    try:
        yield fp
        if create_dir:
            makedirs(dirname)
        os.rename(fp.name, path)
    except:
        with contextlib.suppress():
            os.unlink(fp.name)
        raise
