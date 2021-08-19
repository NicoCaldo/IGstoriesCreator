# Description

The tool will create a standard 1080x1920 JPG image to upload as instagram stories.

The image will have as a background the featured image of an article and as a text the title of the article

The script will find the latest article on the RSS feed of a website via 

```python
feedparser.parse("https://mywebsite/feed/")
```

and will create the image.

As the direct upload on Instagram is not possible, the script will send the image and the link of the article via Pushbullet so, you'll need an API KEY to add in
```python
pb = Pushbullet('myPushubulletAPIKey')
```
You can also choose the font you want to use
```python
font_bold_directory = "myfont.otf"
font_thin_directory = "myfont.otf"
```
As well as the if and the quantity of contrast and enhanchement of the image processed