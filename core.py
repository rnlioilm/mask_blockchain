import collections
import hashlib
import codecs
import base58

def sortedd(unsorted_dict):
    return collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda d: d[0]))

def my_number_hash(self,my_number):
    return hashlib.sha256((hashlib.sha256(my_number.encode()).hexdigest()).encode()).hexdigest()

def gene_add(self,block):
    sha256 = (hashlib.sha256(self._public_key.to_string())).digest()  # publickey(SHA256)
    ripemed160_s = hashlib.new('ripemd160')
    ripemed160_s.update(sha256)
    ripemed160 = codecs.encode(ripemed160_s.digest(), 'hex')
    nb = b'00'  # network byte
    sha256_bpk = hashlib.sha256(codecs.decode(nb + ripemed160, 'hex'))  # bpk (bitcoin public key)
    sha256_2 = (hashlib.sha256(sha256_bpk.digest())).digest()
    sha256_hex = codecs.encode(sha256_2, 'hex')
    checksum = sha256_hex[:8]
    address_hex = ((nb + ripemed160) + checksum).decode('utf-8')
    blockchain_address = base58.b58encode(address_hex).decode('utf-8')
    return blockchain_address