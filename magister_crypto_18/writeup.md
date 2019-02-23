Дана программа, получающая на вход сообщение с паролем и осуществляющая процедуру зашифрования.
Известен шифротекст, нужно получить исходное сообщение.

1. Замечаем, что парольная фраза сворачивается до 3 байт.
2. Рассматриваем процедуру зашифрования

- Сообщение дополняется до длины кратной 14 с помощью PKCS#7 паддинга
- Результат циклически сдвигается на длину len(message) // 3 (целочисленное деление)
- Для каждого блока из 14 байт применяется перестановка по таблице сдвинутая на 7
- На байты результата накладывается гамма из байтов свёрнутого ключа по правилу
```
if i % 3 == 0:
    result.append(ord(permutated_message[i]) ^ passcode[i % 2])
elif i % 3 == 1:
    result.append((ord(permutated_message[i]) + passcode[i % 2]) % 256)
else:
    result.append((ord(permutated_message[i]) - passcode[i % 2]) % 256)
```

3. Будем поочередно обращать все процедуры

Обращаем перестановку по таблице
```
def reverse_permutation(inp):
    PERMUTATION_TABLE = [11, 0, 8, 6, 1, 14, 9, 15, 5, 10, 13, 2, 7, 3, 12, 4]
    out = ["_" for _ in range(len(inp))]
    for i, c in enumerate(inp):
        out[i] = inp[PERMUTATION_TABLE[i]]
    return out
```

Снимаем PKCS#7
```
def pkcs7_decode(text):
    return text[:-text[-1]]
```

4. Создадим функцию ```def decrypt(result_message, passcode):```, которая будет принимать зашифрованный текст и вариант пароля. Процедуру encrypt обращаем снизу вверх.
    
- Обращаем наложение гаммы (XOR не меняется, а + и - меняются местами)
    
```
permutated_message = []
for i in range(len(result_message)):
    if i % 3 == 0:
        permutated_message.append(result_message[i] ^ passcode[i % 2])
    elif i % 3 == 1:
        permutated_message.append((result_message[i] - passcode[i % 2]) % 256)
    else:
        permutated_message.append((result_message[i] + passcode[i % 2]) % 256)
```

- Обращаем перестановки каждого блока (обратите внимание, что сначала выполняется shift, а уже потом reverse_permutation)

```
padded_message = []
for i in range(len(permutated_message) // BLOCK_SIZE):
    new_block = shift(permutated_message[i*BLOCK_SIZE:i*BLOCK_SIZE+BLOCK_SIZE], BLOCK_SIZE // 2)
    padded_message.extend(reverse_permutation(new_block))
```

- Обращаем финальный сдвиг (был на LEN//3, стал на LEN - LEN//3 + 1)
```
padded_message = shift(padded_message, len(padded_message) - len(padded_message) // 3 + 1)
```

- Декодируем PKCS#7 паддинг
```
return pkcs7_decode(padded_message)
```

5. Организуем перебор 2-х байтовой свёртки пароля
```
for a in range(256):
    for b in range(256):
        res = decrypt(enc_message, [a, b])
        if is_ascii(res) and len(res) > 10:
            print(''.join([chr(c) for c in res]))
```

Делаем дополнительное предположение, что результирующее сообщение - ASCII строка из печатаемых символов (чтобы не просматривать вручную все 256^2 вариантов).
```
def is_ascii(s):
    return all(chr(c) in string.printable for c in s)
```

Дополнительно можно проверить, что количество символов результата выше разумного порога: `if is_ascii(res) and len(res) > 10`

Получаем флаг: `the flag is: ##{y0r0wnCrypt0Sh0uldN3v3RBeImpl3m3nt3D}`
