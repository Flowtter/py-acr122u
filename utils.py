def int_list_to_hexadecimal_list(data):
    return [hex(e) for e in data]


def int_list_to_string_list(data):
    return ''.join([chr(e) for e in data])


def replace_arguments(data, arguments):
    if not arguments:
        return data
    result = []
    j = 0
    j_max = len(arguments)
    for i in range(len(data)):
        if data[i] != -1:
            result.append(data[i])
        else:
            if j < j_max:
                arg = arguments[j]
                if type(arg) == int:
                    result.append(arg)
                else:
                    for e in arg:
                        result.append(e)
                j += 1
    return result
