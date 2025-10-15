def is_valid(string):
    stack = []
    char_map = {')': '(', '}': '{', ']': '['}
    for char in string:
        if char in char_map:
            top = stack.pop() if stack else None
            if char_map[char] != top:
                return False
        else:
            stack.append(char)
    return not stack

string = "([{}[]{})"
print(is_valid(string))
