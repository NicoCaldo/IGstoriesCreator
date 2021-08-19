import feedparser
import requests
from lxml import html
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
from io import BytesIO
import text_processing
import math
import os
import time
from pushbullet import Pushbullet

pb = Pushbullet(os.environ['pbk'])

font_bold_directory = "Uni_Sans_Bold.otf"
font_thin_directory = "Uni_Sans_Thin.otf"

#parammetri controllo immagine
do_enhance = True
grey_scale = True

contrast = 0.7 #1 is original image
brightness = 0.6

# trova ultimo articolo
NewsFeed = feedparser.parse("https://thegroovecartel.com/feed/")
entry = NewsFeed.entries[0]
print("Le chiavi del feed sono: ")
print(entry.keys())

# scarica HTML pagina
page = requests.get(entry.link)
extractedHtml = html.fromstring(page.content)

title_list = ['//*[@id="primary"]/div/div/div/main/article/div[2]/div/div[2]/h1',
              '//*[@id="primary"]/div/div/div/main/article/div[1]/div[3]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div[4]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div[3]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div[2]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div/div[2]/h1',
              '//*[@id="primary"]/div/div/div/main/article/div[3]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div[3]/div/div[3]/h1',
              '//*[@id="primary"]/div[1]/div[1]/div[3]/div/div[2]/h1',
              '//*[@id="primary"]/div/div[1]/div/div/article/div[1]/h1',
              '//*[@id="primary"]/div/div/div/main/article/div[2]/div/div[2]/h1',
              '//*[@id="primary"]/div/div/div/main/article/div[1]/div[2]/div/div[2]/h1']
i = 0
title = extractedHtml.xpath(title_list[i])
if not title:
    while not title:
        i += 1
        title = extractedHtml.xpath(title_list[i])

string_title = title[0].text
# estrai sottotitolo

sup_str = title_list[i]
sup_str = sup_str[:-2] + 'p'

sub_title = extractedHtml.xpath(sup_str)

if sub_title:
    string_subtitle = sub_title[0].text
else:
    string_subtitle = ' '

print("Il titolo dell'articolo è: ")
print(string_title)
print("Il sottotitolo dell'articolo è: ")
print(string_subtitle)
# estrai immagine post
print("Immagine del post")
print(entry.media_content[0]['url'])
post_image = entry.media_content[0]['url']

if post_image.find(".jpg") == -1 and post_image.find(".jpeg") == -1:  # controllo se non è immagine
    post_image = entry.media_thumbnail[1]['url']

# rimuovi parti stringa non necessarie
post_image = post_image[38:post_image.find("?")]  # migliorare il codice aggiungendo tutte le possibilità di prefix
post_image = "https://" + post_image

# apro immagine dal web
response = requests.get(post_image)
image = Image.open(BytesIO(response.content))
print("L'immagine originale è: ")
print(image)

# trovo dimensioni
image_width = image.size[0]
image_heigh = image.size[1]

aspect_ratio = (1080, 1920)

# image_heigh è 16
new_image_width = image_heigh / 16 * 9
x_starting_point = (image_width - new_image_width) / 2
# x di partenza, y di partenza, x di arrivo, y di arrivo
box_to_crop = (x_starting_point, 0, new_image_width + x_starting_point, image_heigh)
cropped_image = image.crop(box_to_crop)
resized_image = ImageOps.fit(cropped_image, aspect_ratio)
if grey_scale:
    resized_image = ImageOps.grayscale(resized_image)
print("L'immagine tagliata è: ")
print(cropped_image)
print("L'immagine ridimensionata è: ")
print(resized_image)

if do_enhance:
    # dimezza contrasto
    enhancer = ImageEnhance.Contrast(resized_image)
    resized_image = enhancer.enhance(contrast)
    # dimezza luminosità
    enhancer = ImageEnhance.Brightness(resized_image)
    resized_image = enhancer.enhance(brightness)

# effettivo oggetto disegno per scrivere testo su immagine originale
text_draw = ImageDraw.Draw(resized_image)

title_param = text_processing.text_processing(string_title, font_bold_directory, 72)
subtitle_param = text_processing.text_processing(string_subtitle, font_thin_directory, 48)
print(title_param)
print(subtitle_param)
full_text_heigh = title_param['max_y'] + subtitle_param['max_y'] + 35
coord_y_title = math.ceil((1920 - full_text_heigh) / 2)
coord_y_subtitle = coord_y_title + title_param['max_y'] + 35

white = 0xFFFFFF
text_draw.multiline_text((title_param['x'], coord_y_title), title_param['text'], fill=white, font=title_param['font'],
                         spacing=35, align='center')
text_draw.multiline_text((subtitle_param['x'], coord_y_subtitle), subtitle_param['text'], fill=white,
                         font=subtitle_param['font'], spacing=35, align='center')

root_new_image = time.strftime("%d%m%Y%H%M%S") + ".jpg"

resized_image.save(root_new_image)

# send to pushbullet
my_channel = pb.channels[0]
push = my_channel.push_link('', str(entry.link))
print(push)
with open(root_new_image, "rb") as pic:
    file_data = pb.upload_file(pic, "picture.jpg")
push = my_channel.push_file(**file_data)
print(push)

os.remove(root_new_image)
