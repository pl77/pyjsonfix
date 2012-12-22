#!/usr/bin/python

def _extractString(data):
    if data[0] not in "'\"":  # This isn't a string
        return "", data
    idx = 1
    output = "\""
    is_hex = False
    prev_char = None
    escaped_num = None
    cur_char = data[0]
    quote_char = data[0]
    # While current character isn't a quote or
    # at beginning or previous character is an escape slash
    while 1:
        if idx == len(data):  # Truncated?
            return "Truncated", idx
        prev_char = cur_char
        cur_char = data[idx]
        if cur_char == quote_char and not prev_char == "\\":  # We're at the end quote
            output += "\""
            break
        if escaped_num is not None:
            if cur_char.isdigit():
                idx += 1
                escaped_num += cur_char
            else:  # We're at the end of the escape, put it on the end of the output
                output += "u" + ("0" * 4 + hex(int(escaped_num, 16 if is_hex else 8))[2:])[-4:]
                escaped_num = None
                continue
        else:
            if prev_char == "\\":
                if cur_char in "xu":  # Start of \x or \u escape
                    idx += 1
                    is_hex = True
                    escaped_num = ""
                    continue
                elif cur_char.isdigit():  # Start of octal escape
                    escaped_num = ""
                    is_hex = False
                    continue
            if quote_char == "'" and cur_char == "\"":
                output += "\\"
            output += cur_char
            idx += 1
    return output, idx

def fixJSON(js):
    i = 0
    output = ""
    might_be_a_key = False
    brace_stack = []
    while i < len(js):
        if js[i] in "'\"":  # Found a string
            a, b = _extractString(js[i:])
            output += a
            i += b + 1
        else:
            if js[i] in "{}[]":  # Brace of somesort
                if js[i] in "{[":
                    brace_stack.append(js[i])
                elif js[i] in "]}":
                    if js[i] != {"[": "]", "{": "}"}[brace_stack.pop()]:
                        return "Brace Mismatch", i  # Brace mismatch
                if js[i] == "{":  # Start of a hash, whatever comes next might be a key
                    might_be_a_key = True
                output += js[i]
                i += 1
            elif might_be_a_key and js[i].isalpha():  # Might be a key without quotes
                if js[i] == ",":
                    output += ","
                    i += 1
                keystr = ""
                while js[i] != ":":
                    if js[i].isalnum() or js[i] in "_":
                        if keystr and js[i - 1] == " ":  # Can't have spaces in keys
                            return "Key has space", i - 1
                        keystr += js[i]
                    elif js[i] != " ":  # Some invalid character it seems
                        return "Invalid character", i
                    i += 1
                    if i == len(js):  # Truncated?
                        return "Truncated", i
                keystr = keystr.strip()
                output += "\"%s\":" % keystr.strip()
                i += 1
                might_be_a_key = False
            elif js[i: i + 4] in ["null", "true"]:  # These are valid
                output += js[i:i + 4]
                i += 4
            elif js[i: i + 5] == "false":  # And this
                output += "false"
                i += 5
            elif js[i].isdigit():  # We're a number.
                numstr = ""
                while js[i].lower() in "0123456789abcdefx.":
                    numstr += js[i]
                    i += 1
                    if i == len(js):
                        return "Truncated", i
                base = 10
                if numstr[:2] == "0x":  # We're hex
                    base = 16
                    numstr = numstr[2:]
                elif numstr[0] == "0":  # We're octal
                    base = 8
                if base == 10 and not all([x.isdigit() for x in numstr]):
                    numstr = str(float(numstr))
                else:
                    numstr = str(int(numstr, base))
                if might_be_a_key and brace_stack[-1] != "[":  # We're not in a list
                    output += "\"%s\"" % numstr
                else:
                    output += numstr
            elif js[i] == ",":  # End of a value
                if brace_stack[-1] == "[":  # In a list
                    j = i - 1
                    while js[j] == " ":
                        j -= 1
                    if js[j] == ",":
                        output += "null"
                    if js[i + 1:].strip()[0] == "]":  # List ends with a , so skip it
                        i += js[i + 1:].index("]")
                    else:
                        output += ","
                else:  # Not a list, so next value might be a key
                    output += ","
                    might_be_a_key = True
                i += 1
            else:  # Only some : and spaces should get here
                if js[i] == ":":
                    might_be_a_key = False
                output += js[i]
                i += 1
    return output

