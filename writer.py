from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from datetime import datetime as dt
import requests
import textwrap
import random
import os


class Photo:
    def __init__(self):
        self.width = 1000
        self.height = 700
        self.pos = (self.width, self.height)
        self.all_colors = [(60, 201, 140),  # light green
                           (53, 92, 125),  # dark blue
                           (88, 40, 65),  # violet
                           (0, 150, 136),  # teal 500
                           (255, 152, 0),  # orange 500
                           (30, 136, 229),  # blue 600
                           (216, 27, 96),  # pink 600
                           (0, 77, 64)  # teal 900
                           ]
        self.color = self.get_color()
        self.quote_size = 48
        self.author_size = 60
        self.bottom_size = 36
        self.font_family_path = 'fonts/Roboto-Bold.ttf'
        self.img = Image.new('RGB', self.pos, color=self.color)
        self.draw = ImageDraw.Draw(self.img)
        self.quote_font = ImageFont.truetype(self.font_family_path, size=self.quote_size)
        self.author_font = ImageFont.truetype(self.font_family_path, size=self.author_size)
        self.bottom_font = ImageFont.truetype(self.font_family_path, size=self.bottom_size)
        self.char_width, self.char_height = self.quote_font.getsize('a')
        self.chars_per_line = self.width / self.char_width
        self.hash_tag = '#Automated'
        self.bottom_lines = ['Subscribe to', 'youtube.com/c/GetSetPython']

    def get_color(self):
        return random.choice(self.all_colors)

    @staticmethod
    def get_quote():
        res = requests.get('https://www.brainyquote.com/quotes_of_the_day.html')
        soup = BeautifulSoup(res.text, 'lxml')
        data = soup.find('img', {'class': 'p-qotd'})['alt'].rsplit('-', 1)
        quote, author = data[0].strip(), '- ' + data[1].strip()
        return quote, author

    def write_text(self):
        quote, author = self.get_quote()
        quote_lines = textwrap.wrap(quote, width=self.chars_per_line)
        author_lines = textwrap.wrap(author, width=self.chars_per_line)
        hash_tag = textwrap.wrap(self.hash_tag, width=self.chars_per_line)
        total_lines = len(quote_lines) + len(author_lines) + len(hash_tag)

        print(total_lines + 1, self.height // self.char_height - 7)
        if total_lines + 1 >= self.height // self.char_height - 7:
            return False

        y = (self.height - 1.7 * self.char_height * total_lines - self.char_height) / 4

        for line in quote_lines:
            line_width, line_height = self.quote_font.getsize(line)
            x = (self.width - line_width) / 2
            self.draw.text((x, y), line, font=self.quote_font)
            y += self.char_height * 1.5

        y += self.char_height

        for line in author_lines:
            line_width, line_height = self.quote_font.getsize(line)
            x = (self.width - line_width - 2 * self.char_width) / 2
            self.draw.text((x, y), line, font=self.author_font)
            y += self.char_height * 1.5

        y = self.height - (len(self.bottom_lines) + len(hash_tag) + 1) * self.char_height

        for line in hash_tag:
            line_width, line_height = self.bottom_font.getsize(line)
            x = (self.width - line_width - 2 * self.char_width) / 2
            self.draw.text((x, y), line, font=self.bottom_font)
            y += self.char_height * 1.2

        y += self.char_height / 4

        for line in self.bottom_lines:
            line_width, line_height = self.bottom_font.getsize(line)
            x = (self.width - line_width - 2 * self.char_width) / 2
            self.draw.text((x, y), line, font=self.bottom_font)
            y += self.char_height * 1.2
        return True

    def save_colors(self):
        if not os.path.exists('colors'):
            os.mkdir('colors')
        for color in self.all_colors:
            img = Image.new('RGB', (500, 500), color=color)
            img.save('colors/{}.png'.format(color))

    def show_image(self):
        self.img.show()

    def save_image(self):
        if not os.path.exists('images/'):
            os.mkdir('images/')
        name = str(dt.date(dt.now()))
        self.img.save('images/{}.png'.format(name))

    def main(self):
        try:
            drawn = self.write_text()
            if drawn:
                self.show_image()
                self.save_image()
            else:
                return False
        except:
            pass
        return True


if __name__ == '__main__':
    pic = Photo()
    pic.main()
