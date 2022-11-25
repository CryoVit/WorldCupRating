def barcode_reader(barcode):
    '''
    decode EAN-13 barcode
    _=1, space=0
    '''
    barcode = barcode.replace('_', '1').replace(' ', '0')
    '''
    0-3: start code
    3-9, 10-16, 17-23, 24-30, 31-37, 38-44: Left Hand Odd Parity
    45-49: center guard bars
    50-56, 57-63, 64-70, 71-77, 78-84, 85-91: Right Hand Even Parity
    92-94: end code
    '''
    if barcode[0:3] != '101':
        return None
    if barcode[45:50] != '01010':
        return None
    if barcode[92:95] != '101':
        return None
    '''
    0	0001101	0100111	1110010
    1	0011001	0110011	1100110
    2	0010011	0011011	1101100
    3	0111101	0100001	1000010
    4	0100011	0011101	1011100
    5	0110001	0111001	1001110
    6	0101111	0000101	1010000
    7	0111011	0010001	1000100
    8	0110111	0001001	1001000
    9	0001011	0010111	1110100
    '''
    l_code = ('0001101', '0011001', '0010011', '0111101', '0100011', '0110001', '0101111', '0111011', '0110111', '0001011')
    g_code = ('0100111', '0110011', '0011011', '0100001', '0011101', '0111001', '0000101', '0010001', '0001001', '0010111')
    r_code = ('1110010', '1100110', '1101100', '1000010', '1011100', '1001110', '1010000', '1000100', '1001000', '1110100')
    def decoder(start):
        if barcode[start] == '1':
            for i in range(10):
                if barcode[start:start+7] == r_code[i]:
                    return 2, i
        for i in range(10):
            if barcode[start:start+7] == l_code[i]:
                return 1, i
            if barcode[start:start+7] == g_code[i]:
                return 0, i
        return -1, -1
    result = []
    typer = 0
    if decoder(3)[0] == 0:  # Reverse of R-Code is equal to G-Code
        barcode = barcode[::-1]
    for i in range(3, 45, 7):
        code_type, code = decoder(i)
        if code_type == -1 or code_type == 2:
            return None
        result.append(code)
        typer = typer * 10 + code_type
    for i in range(50, 92, 7):
        code_type, code = decoder(i)
        if code_type != 2:
            return None
        result.append(code)
    '''
    0	LLLLLL	RRRRRR
    1	LLGLGG	RRRRRR
    2	LLGGLG	RRRRRR
    3	LLGGGL	RRRRRR
    4	LGLLGG	RRRRRR
    5	LGGLLG	RRRRRR
    6	LGGGLL	RRRRRR
    7	LGLGLG	RRRRRR
    8	LGLGGL	RRRRRR
    9	LGGLGL	RRRRRR
    '''
    lhand = (111111, 110100, 110010, 110001, 101100, 100110, 100011, 101010, 101001, 100101)
    incode = -1
    for i in range(10):
        if typer == lhand[i]:
            incode = i
            break
    if incode == -1:
        return None
    checksum = incode
    '''
    checksum weight
    (1) 3 1 3 1 3 1 3 1 3 1 3
    '''
    for i in range(11):
        checksum += result[i] * (1 if i % 2 else 3)
    while checksum > 0:
        checksum -= 10
    checksum = -checksum
    if checksum != result[11]:
        return None
    incode = str(incode)
    for i in range(12):
        incode += str(result[i])
    return incode


if __name__ == '__main__':
    
    assert barcode_reader(
        "_ _ ___ __  __  _  _  __ ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __  __ _ _"
    ) == "0712345678911"
    
    assert barcode_reader(
        "_ _ __  __ __  __  _ ___   _  _  _   _    _ _ _ _ _   __ __   _ _ ____ __  _  _  __  __ ___ _ _"
    ) == "0712345678911"
    
    assert barcode_reader(
        '_ _   _ __ _  ___ __  __  _  __ ____ _  ___ _ _ _ __  __ __ __  _    _ _ ___  _  ___ _   _  _ _'
    ) == '5901234123457', '5901234123457'

    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) == '4299687613665', '4299687613665'

    assert barcode_reader(
        '_ _ ___ __  __  _  _  __ ____ _ _   __ __   _ _ _ _ _    _   _  _  _   ___ _  __  __ __ __  _ _'
    ) is None, '0712345678912 : wrong check digit (right: 1)'

    assert barcode_reader(
        '___  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) is None, 'wrong left guard bar'
    
    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ ___ _    __  __ _    _ _ _    _ _    _  ___ _ _'
    ) is None, 'wrong center bar'

    assert barcode_reader(
        '_ _  _  __  _ ___   _ __ _ ____   _  _  _   _ _ _ _ _    __  __ _    _ _ _    _ _    _  ___ ___'
    ) == None, 'wrong right guard bar'

    print("Check done.")

