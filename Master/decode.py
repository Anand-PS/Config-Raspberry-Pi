MORSE_CODE_DICT = { 'A':'._', 'B':'_...',
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

def decrypt(message):
    
    message += ' '  # extra space is added to access the last morse code

    translated_text = ''
    character = ''
    i = 0
    
    for morse_character in message:

        if morse_character != ' ':  # checks for space
            i = 0  # counter to keep track of space
            character += morse_character  # morse code of a single character
        else:
            i += 1 # if i = 1 that indicates a new character

            if i == 2:  # if i = 2 that indicates a new word
                translated_text += ' '  # adding space to separate words
            else:
                try:
                    translated_text += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(character)]
                    character = ''
                except ValueError:
                    print("Invalid morse code! Try again")

    return translated_text