

def coerce_alpha(input):
    '''Default to full opacity'''
    if len(input) == 3:
        input = list(input)
        input.append(255)
    return input
