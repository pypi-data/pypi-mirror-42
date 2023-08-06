from _ethash import ffi, lib


def keccak256(data):
    hash = lib.ethash_keccak256(ffi.from_buffer(data), len(data))
    return ffi.string(hash.bytes)

def keccak512(data):
    hash = lib.ethash_keccak512(ffi.from_buffer(data), len(data))
    return ffi.string(hash.bytes)
