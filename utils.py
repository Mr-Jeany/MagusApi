def replace_placeholders(input_string, placeholders, values):
    for ph_num in range(len(placeholders)):
        input_string = input_string.replace(
            ("%" + str(placeholders[ph_num])),
            str(values[ph_num]))

    return input_string

def multiplaceholder(input_string, placeholder, values):
    input_string = input_string.replace("%%" + str(placeholder), '\n'.join(values))

    return input_string