def lexer(exp):
    exp += '!!!!!!!'
    exp = exp.replace(' ', '')
    arr = []
    i = 0
    while exp[i] != '!':
        c = exp[i]
        if c in '1234567890':
            while exp[i + 1] in '1234567890':
                c += exp[i + 1]
                i += 1
            if exp[i + 1] == '.':
                c += '.'
                i += 1
                while exp[i + 1] in '1234567890':
                    c += exp[i + 1]
                    i += 1
            arr.append(c)
            i += 1
        elif c in '+-*/(),':
            arr.append(c)
            i += 1
        elif exp[i:i + 3] == 'max':
            arr.append('max')
            i += 3
        elif exp[i:i + 3] == 'and':
            arr.append('and')
            i += 3
        else:
            return [], 'неверный символ'
    arr.append('end')
    return arr, ''


def parser_and(tokens, pos):
    left, pos, err = parser_sum_sub(tokens, pos)
    if err != '':
        return 0, pos, err
    while tokens[pos] == 'and':
        pos += 1
        right, pos, err = parser_sum_sub(tokens, pos)
        if err != '':
            return 0, pos, err
        if left != 0 and right != 0:
            left = 1
        else:
            left = 0
    return left, pos, ''


def parser_sum_sub(tokens, pos):
    left, pos, err = parser_mul_dev(tokens, pos)
    if err != '':
        return 0, pos, err
    while tokens[pos] in '+-':
        op = tokens[pos]
        pos += 1
        right, pos, err = parser_mul_dev(tokens, pos)
        if err != '':
            return 0, pos, err
        if op == '+':
            left = left + right
        else:
            left = left - right
    return left, pos, ''


def parser_mul_dev(tokens, pos):
    left, pos, err = parser_plus_minus(tokens, pos)
    if err != '':
        return 0, pos, err
    while tokens[pos] in '*/':
        op = tokens[pos]
        pos += 1
        right, pos, err = parser_plus_minus(tokens, pos)
        if err != '':
            return 0, pos, err
        if op == '*':
            left = left * right
        else:
            if right == 0:
                return 0, pos, 'деление на ноль'
            left = left / right
    return left, pos, ''


def parser_plus_minus(tokens, pos):
    if tokens[pos] == '-':
        value, pos, err = parser_plus_minus(tokens, pos + 1)
        if err != '':
            return 0, pos, err
        return -value, pos, ''
    if tokens[pos] == '+':
        value, pos, err = parser_plus_minus(tokens, pos + 1)
        if err != '':
            return 0, pos, err
        return value, pos, ''
    return parser_last(tokens, pos)


def parser_last(tokens, pos):
    tok = tokens[pos]
    if tok[0] in '1234567890':
        return float(tok), pos + 1, ''
    if tok == '(':
        value, pos, err = parser_and(tokens, pos + 1)
        if err != '':
            return 0, pos, err
        if tokens[pos] != ')':
            return 0, pos, "не хватает ')'"
        return value, pos + 1, ''
    if tok == 'max':
        if tokens[pos + 1] != '(':
            return 0, pos, "не хватает '('"
        pos += 2
        arg = []
        value, pos, err = parser_and(tokens, pos)
        if err != '':
            return 0, pos, err
        arg.append(value)
        while tokens[pos] == ',':
            value, pos, err = parser_and(tokens, pos + 1)
            if err != '':
                return 0, pos, err
            arg.append(value)
        if tokens[pos] != ')':
            return 0, pos, "не хватает ')'"
        m = arg[0]
        for x in arg:
            if x > m:
                m = x
        return m, pos + 1, ''
    return 0, pos, 'лишний токен'


while True:
    exp = input('Введите выражение: ')
    if exp.strip() == "":
        break
    tok, err = lexer(exp)
    if err != '':
        print('Ошибка:', err)
        continue
    result, pos, err = parser_and(tok, 0)
    if err != '':
        print('Ошибка:', err)
        continue
    if tok[pos] != 'end':
        print('Ошибка: лишний токен')
        continue
    if result == int(result):
        print(int(result))
    else:
        print(result)
