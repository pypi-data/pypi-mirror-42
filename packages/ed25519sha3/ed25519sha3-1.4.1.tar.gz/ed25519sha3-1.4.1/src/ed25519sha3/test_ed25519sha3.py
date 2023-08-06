from __future__ import print_function
import sys
import unittest
import time
from binascii import hexlify, unhexlify
import ed25519sha3
from ed25519sha3 import _ed25519 as raw

if sys.version_info[0] == 3:
    def int2byte(i):
        return bytes((i,))
else:
    int2byte = chr

def flip_bit(s, bit=0, in_byte=-1):
    as_bytes = [ord(b) if isinstance(b, str) else b for b in s]
    as_bytes[in_byte] = as_bytes[in_byte] ^ (0x01<<bit)
    return  b"".join([int2byte(b) for b in as_bytes])

# the pure-python demonstration code (on my 2010 MacBookPro) takes 5s to
# generate a public key, 9s to sign, 14s to verify

# the SUPERCOP-ref version we use takes 2ms for keygen, 2ms to sign, and 7ms
# to verify

class Basic(unittest.TestCase):
    timer = None
    def log(self, msg):
        return
        now = time.time()
        if self.timer is None:
            self.timer = now
        else:
            elapsed = now - self.timer
            self.timer = now
            print(" (%f elapsed)" % elapsed)
        print(msg)

    def test_version(self):
        # just make sure it can be retrieved
        ver = ed25519sha3.__version__
        self.failUnless(isinstance(ver, type("")))

    def test_constants(self):
        # the secret key we get from raw.keypair() are 64 bytes long, and
        # are mostly the output of a sha512 call. The first 32 bytes are the
        # private exponent (random, with a few bits stomped).
        self.failUnlessEqual(raw.SECRETKEYBYTES, 64)
        # the public key is the encoded public point
        self.failUnlessEqual(raw.PUBLICKEYBYTES, 32)
        self.failUnlessEqual(raw.SIGNATUREKEYBYTES, 64)

    def test_raw(self):
        sk_s = b"\x00" * 32 # usually urandom(32)
        vk_s, skvk_s = raw.publickey(sk_s)
        self.failUnlessEqual(len(vk_s), 32)
        exp_vks = unhexlify(b"43eeb17f0bab10dd51ab70983c25200a"
                            b"1742d31b3b7b54c38c34d7b827b26eed")
        self.failUnlessEqual(vk_s, exp_vks)
        self.failUnlessEqual(skvk_s[:32], sk_s)
        self.failUnlessEqual(skvk_s[32:], vk_s)
        msg = b"hello world"
        msg_and_sig = raw.sign(msg, skvk_s)
        sig = msg_and_sig[:-len(msg)]
        self.failUnlessEqual(len(sig), 64)
        exp_sig = unhexlify(b"7b34bac4cb2f77c927a127293170ee11"
                            b"3a6dad9ebf9d6b93d4e526d14c74484b"
                            b"68b0f9fedf0d71295302742c81a3a277"
                            b"3f1f9ce7782857834e60e7c843f03b08")
        self.failUnlessEqual(sig, exp_sig)
        ret = raw.open(sig+msg, vk_s) # don't raise exception
        self.failUnlessEqual(ret, msg)
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              sig+msg+b".. NOT!", vk_s)
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              sig+flip_bit(msg), vk_s)
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              sig+msg, flip_bit(vk_s))
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              sig+msg, flip_bit(vk_s, in_byte=2))
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              flip_bit(sig)+msg, vk_s)
        self.failUnlessRaises(raw.BadSignatureError,
                              raw.open,
                              flip_bit(sig, in_byte=33)+msg, vk_s)

    def test_keypair(self):
        sk, vk = ed25519sha3.create_keypair()
        self.failUnless(isinstance(sk, ed25519sha3.SigningKey), sk)
        self.failUnless(isinstance(vk, ed25519sha3.VerifyingKey), vk)
        sk2, vk2 = ed25519sha3.create_keypair()
        self.failIfEqual(hexlify(sk.to_bytes()), hexlify(sk2.to_bytes()))

        # you can control the entropy source
        def not_so_random(length):
            return b"4"*length
        sk1, vk1 = ed25519sha3.create_keypair(entropy=not_so_random)
        self.failUnlessEqual(sk1.to_ascii(encoding="base64"),
                             b"NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ")
        self.failUnlessEqual(vk1.to_ascii(encoding="base64"),
                             b"bSy6m1tnF1ymsneU3/eJldy0fINVqMq/T93H0z7OsNg")
        sk2, vk2 = ed25519sha3.create_keypair(entropy=not_so_random)
        self.failUnlessEqual(sk1.to_ascii(encoding="base64"),
                             sk2.to_ascii(encoding="base64"))
        self.failUnlessEqual(vk1.to_ascii(encoding="base64"),
                             vk2.to_ascii(encoding="base64"))


    def test_publickey(self):
        seed = unhexlify(b"4ba96b0b5303328c7405220598a587c4"
                         b"acb06ed9a9601d149f85400195f1ec3d")
        sk = ed25519sha3.SigningKey(seed)
        self.failUnlessEqual(hexlify(sk.to_bytes()),
                             (b"4ba96b0b5303328c7405220598a587c4"
                              b"acb06ed9a9601d149f85400195f1ec3d"
                              b"8277bdf8fdf511c7494096a60e117ec0"
                              b"34aa5d79e3d08354e02029315841670e"))
        self.failUnlessEqual(hexlify(sk.to_seed()),
                             (b"4ba96b0b5303328c7405220598a587c4"
                              b"acb06ed9a9601d149f85400195f1ec3d"))
        self.failUnlessRaises(ValueError,
                              ed25519sha3.SigningKey, b"wrong length")
        sk2 = ed25519sha3.SigningKey(seed)
        self.failUnlessEqual(sk, sk2)

    def test_OOP(self):
        sk_s = unhexlify(b"4ba96b0b5303328c7405220598a587c4"
                         b"acb06ed9a9601d149f85400195f1ec3d"
                         b"8277bdf8fdf511c7494096a60e117ec0"
                         b"34aa5d79e3d08354e02029315841670e")
        sk = ed25519sha3.SigningKey(sk_s)
        self.failUnlessEqual(len(sk.to_bytes()), 64)
        self.failUnlessEqual(sk.to_bytes(), sk_s)

        sk2_seed = unhexlify(b"4ba96b0b5303328c7405220598a587c4"
                             b"acb06ed9a9601d149f85400195f1ec3d")
        sk2 = ed25519sha3.SigningKey(sk2_seed)
        self.failUnlessEqual(sk2.to_bytes(), sk.to_bytes())

        vk = sk.get_verifying_key()
        self.failUnlessEqual(len(vk.to_bytes()), 32)
        exp_vks = unhexlify(b"8277bdf8fdf511c7494096a60e117ec0"
                            b"34aa5d79e3d08354e02029315841670e")
        self.failUnlessEqual(vk.to_bytes(), exp_vks)
        self.failUnlessEqual(ed25519sha3.VerifyingKey(vk.to_bytes()), vk)
        msg = b"hello world"
        sig = sk.sign(msg)
        self.failUnlessEqual(len(sig), 64)
        exp_sig = unhexlify(b"63a7c076fdebced5fb96ceb66acf4458"
                            b"5df6212819d68235294f805ec6bce868"
                            b"add51cb345cc4fe7ab5d21bbc711a362"
                            b"a6f47bc71e36e917d565e2e88558ae06")
        self.failUnlessEqual(sig, exp_sig)
        self.failUnlessEqual(vk.verify(sig, msg), None) # also, don't throw
        self.failUnlessRaises(ed25519sha3.BadSignatureError,
                              vk.verify, sig, msg+b".. NOT!")

    def test_object_identity(self):
        sk1_s = unhexlify(b"ef32972ae3f1252a5aa1395347ea008c"
                          b"bd2fed0773a4ea45e2d2d06c8cf8fbd4"
                          b"54225d32ccd9a8b47843bb5312240a5f"
                          b"44c943b2f4fef1f32507c7e7394a983f")
        sk2_s = unhexlify(b"3d550c158900b4c2922b6656d2f80572"
                          b"89de4ee65043745179685ae7d29b944d"
                          b"e258ab671334001099dc005366d41de2"
                          b"de4228038aab75f9ca004197dcc2b7a0")
        sk1a = ed25519sha3.SigningKey(sk1_s)
        sk1b = ed25519sha3.SigningKey(sk1_s)
        vk1a = sk1a.get_verifying_key()
        vk1b = sk1b.get_verifying_key()
        sk2 = ed25519sha3.SigningKey(sk2_s)
        vk2 = sk2.get_verifying_key()
        self.failUnlessEqual(sk1a, sk1b)
        self.failIfEqual(sk1a, sk2)
        self.failUnlessEqual(vk1a, vk1b)
        self.failIfEqual(vk1a, vk2)

        self.failIfEqual(sk2, b"not a SigningKey")
        self.failIfEqual(vk2, b"not a VerifyingKey")

    def test_prefix(self):
        sk1,vk1 = ed25519sha3.create_keypair()
        PREFIX = b"private0-"
        p = sk1.to_bytes(PREFIX)
        # that gives us a binary string with a prefix
        self.failUnless(p[:len(PREFIX)] == PREFIX, repr(p))
        sk2 = ed25519sha3.SigningKey(p, prefix=PREFIX)
        self.failUnlessEqual(sk1, sk2)
        self.failUnlessEqual(repr(sk1.to_bytes()), repr(sk2.to_bytes()))
        self.failUnlessRaises(ed25519sha3.BadPrefixError,
                              ed25519sha3.SigningKey, p, prefix=b"WRONG-")
        # SigningKey.to_seed() can do a prefix too
        p = sk1.to_seed(PREFIX)
        self.failUnless(p[:len(PREFIX)] == PREFIX, repr(p))
        sk3 = ed25519sha3.SigningKey(p, prefix=PREFIX)
        self.failUnlessEqual(sk1, sk3)
        self.failUnlessEqual(repr(sk1.to_bytes()), repr(sk3.to_bytes()))
        self.failUnlessRaises(ed25519sha3.BadPrefixError,
                              ed25519sha3.SigningKey, p, prefix=b"WRONG-")

        # verifying keys can do this too
        PREFIX = b"public0-"
        p = vk1.to_bytes(PREFIX)
        self.failUnless(p.startswith(PREFIX), repr(p))
        vk2 = ed25519sha3.VerifyingKey(p, prefix=PREFIX)
        self.failUnlessEqual(vk1, vk2)
        self.failUnlessEqual(repr(vk1.to_bytes()), repr(vk2.to_bytes()))
        self.failUnlessRaises(ed25519sha3.BadPrefixError,
                              ed25519sha3.VerifyingKey, p, prefix=b"WRONG-")

        # and signatures
        PREFIX = b"sig0-"
        p = sk1.sign(b"msg", PREFIX)
        self.failUnless(p.startswith(PREFIX), repr(p))
        vk1.verify(p, b"msg", PREFIX)
        self.failUnlessRaises(ed25519sha3.BadPrefixError,
                              vk1.verify, p, b"msg", prefix=b"WRONG-")

    def test_ascii(self):
        b2a = ed25519sha3.to_ascii
        a2b = ed25519sha3.from_ascii
        for prefix in ("", "prefix-"):
            for length in range(0, 100):
                b1 = b"a"*length
                for base in ("base64", "base32", "base16", "hex"):
                    a = b2a(b1, prefix, base)
                    b2 = a2b(a, prefix, base)
                    self.failUnlessEqual(b1, b2)

    def test_encoding(self):
        sk_s = b"\x88" * 32 # usually urandom(32)
        sk1 = ed25519sha3.SigningKey(sk_s)
        vk1 = sk1.get_verifying_key()

        def check1(encoding, expected):
            PREFIX = "private0-"
            p = sk1.to_ascii(PREFIX, encoding)
            self.failUnlessEqual(p, expected)
            sk2 = ed25519sha3.SigningKey(p, prefix=PREFIX, encoding=encoding)
            self.failUnlessEqual(repr(sk1.to_bytes()), repr(sk2.to_bytes()))
            self.failUnlessEqual(sk1, sk2)

        check1("base64", b"private0-iIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIg")
        check1("base32", b"private0-rceirceirceirceirceirceirceirceirceirceirceirceircea")
        check1("hex", b"private0-8888888888888888888888888888888888888888888888888888888888888888")

        def check2(encoding, expected):
            PREFIX="public0-"
            p = vk1.to_ascii(PREFIX, encoding)
            self.failUnlessEqual(p, expected)
            vk2 = ed25519sha3.VerifyingKey(p, prefix=PREFIX, encoding=encoding)
            self.failUnlessEqual(repr(vk1.to_bytes()), repr(vk2.to_bytes()))
            self.failUnlessEqual(vk1, vk2)
        check2("base64", b"public0-dBFqz6Fh4eYOn3nop4hvfHm9hmAmG3VXizOjECjqiSs")
        check2("base32", b"public0-oqiwvt5bmhq6mdu7phukpcdppr433btaeynxkv4lgorrakhkrevq")
        check2("hex", b"public0-74116acfa161e1e60e9f79e8a7886f7c79bd8660261b75578b33a31028ea892b")

        def check3(encoding, expected):
            msg = b"msg"
            PREFIX="sig0-"
            sig = sk1.sign(msg, PREFIX, encoding)
            self.failUnlessEqual(sig, expected)
            vk1.verify(sig, msg, PREFIX, encoding)
        check3("base64", b"sig0-VPXvzJkesg6kPvNWX0UxQ92z2ZccZf5Dk1YNzxVsix6W7+iCQCdCfiDrnxqqqHe1Q6jzTJCmoc1xBeEfdOnODQ")
        check3("base32", b"sig0-kt267tezd2za5jb66nlf6rjripo3hwmxdrs74q4tkyg46flmrmpjn37iqjacoqt6edvz6gvkvb33kq5i6ngjbjvbzvyqlyi7otu44di")
        check3("hex", b"sig0-54f5efcc991eb20ea43ef3565f453143ddb3d9971c65fe4393560dcf156c8b1e96efe8824027427e20eb9f1aaaa877b543a8f34c90a6a1cd7105e11f74e9ce0d")


if __name__ == '__main__':
    unittest.main()
