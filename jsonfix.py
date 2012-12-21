#!/usr/bin/python

def fixJSON(js):
    i = 0
    out = ""
    maybekey = False
    stack = []
    while i < len(js):
        if js[i] in "'\"":  # Found a string
            qchar = js[i]
            out += "\""
            i += 1
            ishex = False
            escaped_num = None
            while js[i - 1] == "\\" or js[i] != qchar:
                if escaped_num is not None:
                    i += 1
                    if js[i].isdigit():
                        escaped_num += js[i]
                    else:
                        out += "u" + ("0" * 4 + hex(int(escaped_num, 16 if ishex else 8))[2:])[-4:]
                        escaped_num = None
                        ishex = False
                        continue
                else:
                    if js[i - 1] == "\\":
                        if js[i] == "x" or js[i] == "u":
                            escaped_num = ""
                            i += 1
                            ishex = True
                            continue
                        elif js[i].isdigit():
                            escaped_num = js[i]
                            continue
                    if js[i] == "\"" and js[i - 1] != "\\":
                        out += "\\"
                    out += js[i]
                    i += 1
                    if i == len(js):  # Truncated?
                        return "Truncated", i
            out += "\""
            i += 1
            maybekey = False
        else:
            if js[i] in "{}[]":  # Brace of somesort
                if js[i] in "{[":
                    stack.append(js[i])
                elif js[i] in "]}":
                    if js[i] != {"[": "]", "{": "}"}[stack.pop()]:
                        return "Brace Mismatch", i  # Brace mismatch
                if js[i] == "{":  # Start of a hash, whatever comes next might be a key
                    maybekey = True
                if js[i] == "]":  # End of list
                    j = i - 1
                    while js[j] == " ":
                        j -= 1
                    if js[j] == ",":   # List ended with ,
                        out += "null"
                out += js[i]
                i += 1
            elif maybekey and js[i].isalpha():  # Might be a key without quotes
                if js[i] == ",":
                    out += ","
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
                out += "\"%s\":" % keystr.strip()
                i += 1
                maybekey = False
            elif (i + 4 < len(js)) and js[i: i + 4] in ["null", "true"]:  # These are valid
                out += js[i:i + 4]
                i += 4
            elif (i + 5 < len(js)) and js[i:i + 5] == "false":  # And this
                out += "false"
                i += 5
            elif js[i].isdigit():  # We're a number
                numstr = ""
                while js[i].lower() in "0123456789abcdefx.":
                    numstr += js[i]
                    i += 1
                    if i == len(js):
                        return "Truncated", i
                try:
                    numstr = str(eval(numstr))  # Could be octal or hex
                except:
                    return "Fail number", i
                if maybekey and stack[-1] != "[":  # We're not in a list
                    out += "\"%s\"" % numstr
                else:
                    out += numstr
            elif js[i] == ",":  # End of a value
                j = i - 1
                while js[j] == " ":
                    j -= 1
                if js[j] == ",":  # Last value was empty, probably in a list, put a null
                    out += "null"
                out += ","
                maybekey = True
                i += 1
            else:  # Only some : and spaces should get here
                if js[i] == ":":
                    maybekey = False
                out += js[i]
                i += 1
    return out

