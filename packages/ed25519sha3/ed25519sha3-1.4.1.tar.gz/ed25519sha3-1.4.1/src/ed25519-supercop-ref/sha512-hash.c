/*
RHash.
Modified by Alex Huszagh.
Modified from the RHash license to the MIT license.
*/

#include "sha512.h"
#include <assert.h>
#include <stdint.h>
#include <string.h>

#define SHA3_MAX_PERMUTATION_SIZE 25
#define QWORDS 24
#define SHA3_ROUNDS 24

static const uint64_t KECCAK_ROUND_CONSTANTS[SHA3_ROUNDS] = {
    0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808AULL, 0x8000000080008000ULL,
    0x000000000000808BULL, 0x0000000080000001ULL, 0x8000000080008081ULL, 0x8000000000008009ULL,
    0x000000000000008AULL, 0x0000000000000088ULL, 0x0000000080008009ULL, 0x000000008000000AULL,
    0x000000008000808BULL, 0x800000000000008BULL, 0x8000000000008089ULL, 0x8000000000008003ULL,
    0x8000000000008002ULL, 0x8000000000000080ULL, 0x000000000000800AULL, 0x800000008000000AULL,
    0x8000000080008081ULL, 0x8000000000008080ULL, 0x0000000080000001ULL, 0x8000000080008008ULL
};

typedef struct {
    uint64_t hash[SHA3_MAX_PERMUTATION_SIZE];
    uint64_t message[QWORDS];
    uint32_t rest;
    uint32_t block_size;
} sha3_context;

#define ROTL64(qword, n) ((qword) << (n) ^ ((qword) >> (64 - (n))))
#define IS_ALIGNED_64(p) (0 == (((uintptr_t) p) & 7))

static uint64_t le64_to_h(uint64_t v) {
    unsigned char* buf;
    buf = (unsigned char*) &v;
    return (
        ((uint64_t) buf[0]) |
        (((uint64_t) buf[1]) << 8) |
        (((uint64_t) buf[2]) << 16) |
        (((uint64_t) buf[3]) << 24) |
        (((uint64_t) buf[4]) << 32) |
        (((uint64_t) buf[5]) << 40) |
        (((uint64_t) buf[6]) << 48) |
        (((uint64_t) buf[7]) << 56)
    );
}


static uint64_t h_to_le64(uint64_t v) {
    unsigned char* buf;
    uint64_t u;
    buf = (unsigned char*) &u;
    buf[0] = (unsigned char) (v & 0XFF);
    buf[1] = (unsigned char) ((v >> 8) & 0XFF);
    buf[2] = (unsigned char) ((v >> 16) & 0XFF);
    buf[3] = (unsigned char) ((v >> 24) & 0XFF);
    buf[4] = (unsigned char) ((v >> 32) & 0XFF);
    buf[5] = (unsigned char) ((v >> 40) & 0XFF);
    buf[6] = (unsigned char) ((v >> 48) & 0XFF);
    buf[7] = (unsigned char) ((v >> 56) & 0XFF);

    return u;
}


static void* memcpy_h_to_le64(void* dst, const void* src, size_t num) {
    size_t i;
    uint64_t* dst_;
    const uint64_t* src_;

    dst_ = (uint64_t*) dst;
    src_ = (uint64_t*) src;
    for (i = 0; i < num / 8; i++) {
        dst_[i] = h_to_le64(src_[i]);
    }

    return dst;
}


static void keccak_init(sha3_context* ctx, uint32_t bits) {
    /* NB: The Keccak capacity parameter = bits * 2 */
    uint32_t rate = 1600 - bits * 2;

    memset(ctx, 0, sizeof(sha3_context));
    ctx->block_size = rate / 8;
    assert(rate <= 1600 && (rate % 64) == 0);
}


static void sha3_512_init(sha3_context* ctx) {
    keccak_init(ctx, 512);
}


/*
 *  Keccak theta() transformation
 */
static void keccak_theta(uint64_t *A) {
    unsigned int x;
    uint64_t C[5], D[5];

    for (x = 0; x < 5; x++) {
        C[x] = A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20];
    }
    D[0] = ROTL64(C[1], 1) ^ C[4];
    D[1] = ROTL64(C[2], 1) ^ C[0];
    D[2] = ROTL64(C[3], 1) ^ C[1];
    D[3] = ROTL64(C[4], 1) ^ C[2];
    D[4] = ROTL64(C[0], 1) ^ C[3];

    for (x = 0; x < 5; x++) {
        A[x]      ^= D[x];
        A[x + 5]  ^= D[x];
        A[x + 10] ^= D[x];
        A[x + 15] ^= D[x];
        A[x + 20] ^= D[x];
    }
}

/*
 *  Keccak pi() transformation
 */
static void keccak_pi(uint64_t *A) {
    uint64_t A1;
    A1 = A[1];
    A[ 1] = A[ 6];
    A[ 6] = A[ 9];
    A[ 9] = A[22];
    A[22] = A[14];
    A[14] = A[20];
    A[20] = A[ 2];
    A[ 2] = A[12];
    A[12] = A[13];
    A[13] = A[19];
    A[19] = A[23];
    A[23] = A[15];
    A[15] = A[ 4];
    A[ 4] = A[24];
    A[24] = A[21];
    A[21] = A[ 8];
    A[ 8] = A[16];
    A[16] = A[ 5];
    A[ 5] = A[ 3];
    A[ 3] = A[18];
    A[18] = A[17];
    A[17] = A[11];
    A[11] = A[ 7];
    A[ 7] = A[10];
    A[10] = A1;
    // note: A[ 0] is left as is
}

/* Keccak chi() transformation */
static void keccak_chi(uint64_t *A) {
    int i;
    for (i = 0; i < 25; i += 5) {
        uint64_t A0 = A[0 + i], A1 = A[1 + i];
        A[0 + i] ^= ~A1 & A[2 + i];
        A[1 + i] ^= ~A[2 + i] & A[3 + i];
        A[2 + i] ^= ~A[3 + i] & A[4 + i];
        A[3 + i] ^= ~A[4 + i] & A0;
        A[4 + i] ^= ~A0 & A1;
    }
}


static void sha3_permutation(uint64_t *state) {
    int r;
    for (r = 0; r < SHA3_ROUNDS; r++)
    {
        keccak_theta(state);

        // apply Keccak rho() transformation
        state[ 1] = ROTL64(state[ 1],  1);
        state[ 2] = ROTL64(state[ 2], 62);
        state[ 3] = ROTL64(state[ 3], 28);
        state[ 4] = ROTL64(state[ 4], 27);
        state[ 5] = ROTL64(state[ 5], 36);
        state[ 6] = ROTL64(state[ 6], 44);
        state[ 7] = ROTL64(state[ 7],  6);
        state[ 8] = ROTL64(state[ 8], 55);
        state[ 9] = ROTL64(state[ 9], 20);
        state[10] = ROTL64(state[10],  3);
        state[11] = ROTL64(state[11], 10);
        state[12] = ROTL64(state[12], 43);
        state[13] = ROTL64(state[13], 25);
        state[14] = ROTL64(state[14], 39);
        state[15] = ROTL64(state[15], 41);
        state[16] = ROTL64(state[16], 45);
        state[17] = ROTL64(state[17], 15);
        state[18] = ROTL64(state[18], 21);
        state[19] = ROTL64(state[19],  8);
        state[20] = ROTL64(state[20], 18);
        state[21] = ROTL64(state[21],  2);
        state[22] = ROTL64(state[22], 61);
        state[23] = ROTL64(state[23], 56);
        state[24] = ROTL64(state[24], 14);

        keccak_pi(state);
        keccak_chi(state);

        // apply iota(state, r)
        *state ^= KECCAK_ROUND_CONSTANTS[r];
    }
}

/**
 *  The core transformation. Process the specified block of data.
 */
static void sha3_process_block(uint64_t* hash, const uint64_t* block, size_t block_size) {
    /* expanded loop */
    hash[ 0] ^= le64_to_h(block[ 0]);
    hash[ 1] ^= le64_to_h(block[ 1]);
    hash[ 2] ^= le64_to_h(block[ 2]);
    hash[ 3] ^= le64_to_h(block[ 3]);
    hash[ 4] ^= le64_to_h(block[ 4]);
    hash[ 5] ^= le64_to_h(block[ 5]);
    hash[ 6] ^= le64_to_h(block[ 6]);
    hash[ 7] ^= le64_to_h(block[ 7]);
    hash[ 8] ^= le64_to_h(block[ 8]);
    /* if not sha3-512 */
    if (block_size > 72) {
        hash[ 9] ^= le64_to_h(block[ 9]);
        hash[10] ^= le64_to_h(block[10]);
        hash[11] ^= le64_to_h(block[11]);
        hash[12] ^= le64_to_h(block[12]);
        /* if not sha3-384 */
        if (block_size > 104) {
            hash[13] ^= le64_to_h(block[13]);
            hash[14] ^= le64_to_h(block[14]);
            hash[15] ^= le64_to_h(block[15]);
            hash[16] ^= le64_to_h(block[16]);
            /* if not sha3-256 */
            if (block_size > 136) {
                hash[17] ^= le64_to_h(block[17]);
                /* if not sha3-224 */
                if (block_size > 144) {
                    hash[18] ^= le64_to_h(block[18]);
                    hash[19] ^= le64_to_h(block[19]);
                    hash[20] ^= le64_to_h(block[20]);
                    hash[21] ^= le64_to_h(block[21]);
                    hash[22] ^= le64_to_h(block[22]);
                    hash[23] ^= le64_to_h(block[23]);
                    hash[24] ^= le64_to_h(block[24]);
                }
            }
        }
    }
    // make a permutation of the hash
    sha3_permutation(hash);
}


/**
 *  Calculate message hash.
 *  Can be called repeatedly with chunks of the message to be hashed.
 */
static void sha3_update(void* ptr, const void *buf, size_t size) {
    sha3_context* ctx;
    const uint8_t* msg;
    size_t index;
    size_t block_size;
    size_t left;
    uint64_t* aligned_message_block;

    ctx = (sha3_context*) ptr;
    msg = (const uint8_t*) buf;
    index = (size_t)ctx->rest;
    block_size = (size_t)ctx->block_size;

    ctx->rest = (unsigned)((ctx->rest + size) % block_size);

    // fill partial block
    if (index) {
        left = block_size - index;
        memcpy((char*)ctx->message + index, msg, (size < left ? size : left));
        if (size < left) {
            return;
        }

        // process partial block
        sha3_process_block(ctx->hash, ctx->message, block_size);
        msg  += left;
        size -= left;
    }
    while (size >= block_size) {
        if (IS_ALIGNED_64(msg)) {
            /* the most common case is processing of an already aligned message
            without copying it */
            aligned_message_block = (uint64_t*)msg;
        } else {
            memcpy(ctx->message, msg, block_size);
            aligned_message_block = ctx->message;
        }

        sha3_process_block(ctx->hash, aligned_message_block, block_size);
        msg  += block_size;
        size -= block_size;
    }
    if (size) {
        memcpy(ctx->message, msg, size); // save leftovers
    }
}


/**
 *  Store calculated hash into the given array.
 */
static void sha3_final(void* ptr, void* buf) {
    sha3_context* ctx;
    uint8_t* result;
    size_t digest_length;
    size_t block_size;

    ctx = (sha3_context*) ptr;
    result = (uint8_t*) buf;
    digest_length = 100 - ctx->block_size / 2;
    block_size = ctx->block_size;

    // clear the rest of the data queue
    memset((char*)ctx->message + ctx->rest, 0, block_size - ctx->rest);
    ((char*)ctx->message)[ctx->rest] |= 0x06;
    ((char*)ctx->message)[block_size - 1] |= 0x80;

    // process final block
    sha3_process_block(ctx->hash, ctx->message, block_size);

    assert(block_size > digest_length);
    if (result) {
        memcpy_h_to_le64(result, ctx->hash, digest_length);
    }

    memset(&digest_length, 0, sizeof(digest_length));
    memset(&block_size, 0, sizeof(block_size));
    memset(ctx, 0, sizeof(*ctx));
}


int crypto_hash_sha3_512(unsigned char *out, const unsigned char *in, unsigned long long inlen)
{
    sha3_context ctx;
    sha3_512_init(&ctx);
    sha3_update(&ctx, in, inlen);
    sha3_final(&ctx, out);
    memset(&ctx, 0, sizeof(sha3_context));

    return 0;
}
