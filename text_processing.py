from PIL import Image, ImageDraw, ImageFont
import math
import re


def text_processing(string_title, font_directory, font_size):
    # creo immagine fasulla per stringa
    im = Image.new(mode="RGB", size=(0, 0))
    draw = ImageDraw.Draw(im)

    # ricava font
    fnt_bold = ImageFont.truetype(font_directory, font_size)
    text_size_one_row = draw.textsize(string_title.upper(), font=fnt_bold)
    print(f"Il numero di pixel del testo è: {text_size_one_row}")
    numero_righe = math.ceil(text_size_one_row[0] / 820)
    print(f"Il numero di righe del testo è: {numero_righe}")

    string_title_len = len(string_title)
    string_title_upper = string_title.upper()
    char_per_row = math.ceil(string_title_len / numero_righe)

    print(f"Caratteri per riga {char_per_row}")

    # indice spazi
    res = [i.start() for i in re.finditer(" ", string_title_upper)]

    print(f"Spazi in posizione {res}")

    j = 0
    k = 0
    indice_precedente = 0
    array_testo = []
    for i in range(1, numero_righe):
        while res[k] < char_per_row * i:
            k += 1
        indice_successivo = res[k - 1]
        if i == 1:
            testo = string_title_upper[indice_precedente:indice_successivo]
        else:
            testo = string_title_upper[indice_precedente + 1:indice_successivo]
        print(testo)
        array_testo.append(testo)
        j += 1
        # aggiorno indici
        indice_precedente = indice_successivo
    testo = string_title_upper[indice_precedente + 1:]
    print(testo)
    array_testo.append(testo)
    print(array_testo)

    max_len = len(array_testo[0])
    max_index = 0
    for i in range(1, len(array_testo)):
        if len(array_testo[i]) > max_len:
            max_index = i
            max_len = len(array_testo[i])
    print(f"Indice stringa a lunghezza massima {max_index} con {max_len} caratteri")

    # trovo dimensione stringa lunghezza massima per calcolo
    text_size_logest_row = draw.textsize(array_testo[max_index], font=fnt_bold)
    print(f"lunghezza {text_size_logest_row} in pixel")
    # calcolo punto di partenza lungo x
    x_starting_point = math.ceil((1080 - text_size_logest_row[0]) / 2)
    print(f"x di partenza {x_starting_point}")

    # riporto il testo in una singola riga
    inline_title_text = ""
    for i in range(0, len(array_testo)):
        if i < len(array_testo) - 1:
            inline_title_text = inline_title_text + array_testo[i] + "\n"
        else:
            inline_title_text = inline_title_text + array_testo[i]
    print(inline_title_text)

    # trovo altezza totale del testo
    max_heigh_title_text = (text_size_logest_row[1] * numero_righe) + (
                35 * (numero_righe - 1))  # 35 è lo spacing di multiline_text
    print(f"Altezza in pixel del titolo {max_heigh_title_text}")

    output = dict()
    output['x'] = x_starting_point
    output['text'] = inline_title_text
    output['font'] = fnt_bold
    output['max_y'] = max_heigh_title_text

    return output
