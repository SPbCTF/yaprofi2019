def fold(passphrase):
    """
    Fold the passphrase to the fixed 2-bytes block
    :param passphrase: ascii string passphrase
    :return: array of two integer elements
    """
    block = [0, 0]
    for i in range(len(passphrase)):
        block[i % 2] = (block[i % 2] + ord(passphrase[i])) % 256
    return block


def encrypt(message, passcode):
    """
    Encrypt message with the passcode
    :param message: ascii string message
    :param passcode: array of integers with the length of 2
    :return: array of integers representing encrypted message
    """
    result = []

    for i in range(len(message)):
        if i % 3 == 0:
            result.append(ord(message[i]) ^ passcode[i % 2])
        elif i % 3 == 1:
            result.append((ord(message[i]) + passcode[i % 2]) % 256)
        else:
            result.append((ord(message[i]) - passcode[i % 2]) % 256)

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
