CHARS_TO_MORSE_CODE_MAP = { 'A':'._', 'B':'_...',
                    'C':'_._.', 'D':'_..', 'E':'.',
                    'F':'.._.', 'G':'__.', 'H':'....',
                    'I':'..', 'J':'.___', 'K':'_._',
                    'L':'._..', 'M':'__', 'N':'_.',
                    'O':'___', 'P':'.__.', 'Q':'__._',
                    'R':'._.', 'S':'...', 'T':'_',
                    'U':'.._', 'V':'..._', 'W':'.__',
                    'X':'_.._', 'Y':'_.__', 'Z':'__..',
                    '1':'.____', '2':'..___', '3':'...__',
                    '4':'...._', '5':'.....', '6':'_....',
                    '7':'__...', '8':'___..', '9':'____.',
                    '0':'_____', ', ':'__..__', '.':'._._._',
                    '?':'..__..', '/':'_.._.', '_':'_...._',
                    '(':'_.__.', ')':'_.__._'}

notDefined = ["'"]

def encrypt(english_plain_text):
    morseCode = ''

    for char in english_plain_text:
        # checking for space
        # to add single space after every character and double space after every word
        if char == ' ':
            morseCode += '  '
        else:
            # adding encoded morse code to the result
            if char in notDefined:
                morseCode += ' '
                continue
            morseCode += CHARS_TO_MORSE_CODE_MAP[char.upper()] + ' '
    return morseCode