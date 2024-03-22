
def svg_string(name):
    try:
        with open(f'./img/{name}.svg', 'r') as file:
            return file.read().replace('"', "\'")
    except:
        return ''
