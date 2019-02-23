BLOCK_SIZE = 14


def pkcs7_encode(text):
    """
    Pad an input string according to PKCS#7
    :param text: ascii string
    :return out: binary padded string
    """
    l = len(text)
    val = BLOCK_SIZE - (l % BLOCK_SIZE)
    return text + chr(val) * val


def permutation(inp):
    """
    Apply permutation procedure
    :param inp: input block of ascii letters with length equals to BLOCK_SIZE
    :return: out: permutated block with the length of BLOCK_SIZE
    """
    PERMUTATION_TABLE = [11, 0, 8, 6, 1, 9, 5, 10, 13, 2, 7, 3, 12, 4]

    # throw exception if the input length is not equal to 16
    assert len(inp) == BLOCK_SIZE

    out = ["_" for _ in range(len(inp))]
    for i, c in enumerate(inp):
        out[PERMUTATION_TABLE[i]] = c
    return out


def fold(passphrase):
    """
    Fold the passphrase to the fixed 2-bytes block
    :param passphrase: ascii string passphrase
    :return: array of two integer elements
    """
    block = [0, 0]
    for i in range(len(passphrase)):
        block[i % 2] = (block[i % 2] ^ ord(passphrase[i])) % 256
    return block


def shift(message, n):
    """
    Apply cyclic shift of the array
    :param message: array of bytes
    :param n: shift number
    :return: Shifted array of bytes
    """
    return message[-n:] + message[:-n]


def encrypt(message, passcode):
    """
    Encrypt message with the passcode
    :param message: ascii string message
    :param passcode: array of integers with the length of 2
    :return: array of integers representing encrypted message
    """
    result = []

    padded_message = shift(pkcs7_encode(message), len(message) // 3)
    permutated_message = []
    for i in range(len(padded_message) // BLOCK_SIZE):
        new_block = permutation(padded_message[i*BLOCK_SIZE:i*BLOCK_SIZE+BLOCK_SIZE])
        permutated_message.extend(shift(new_block, len(new_block) // 2))

    for i in range(len(permutated_message)):
        if i % 3 == 0:
            result.append(ord(permutated_message[i]) ^ passcode[i % 2])
        elif i % 3 == 1:
            result.append((ord(permutated_message[i]) + passcode[i % 2]) % 256)
        else:
            result.append((ord(permutated_message[i]) - passcode[i % 2]) % 256)

    return result


if __name__ == "__main__":
    passphrase = input("Input passphrase: ")
    message = input("Input message: ")

    passcode = fold(passphrase)
    enc_message = encrypt(message, passcode)

    enc_message_printable = ''.join([chr(c) for c in enc_message])
    print("message: {}\nencrypted message: {}\nstring representation of the encrypted message: {}".format(message,
                                                                                                          enc_message,
                                                                                                          enc_message_printable))
