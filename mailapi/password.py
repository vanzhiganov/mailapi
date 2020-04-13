from hashlib import md5, sha1, sha512
from base64 import b64encode, b64decode
from . import md5crypt
from .helpers import generate_random_strings

# see also: https://github.com/iredmail/iRedAdmin/blob/93d6de44d77bbd9e039444a86e9b2cc83ee8dc2e/libs/iredutils.py#L419


def generate_md5_password(p):
    p = str(p).strip()
    return md5crypt.unix_md5_crypt(p, generate_random_strings(length=8))


def generate_sha512_password(p: str):
    """Generate SHA512 password with prefix '{SHA512}'."""
    pw = sha512(p.strip().encode())
    return "".join(['{SHA512}', b64encode(pw.digest()).decode()])
