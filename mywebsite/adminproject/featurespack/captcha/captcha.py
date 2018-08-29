import random
from PIL import Image,ImageDraw,ImageFont, ImageFilter
import os


class Captcha(object):
        __letter_cases = "abcdefghijklmnopqrstuvwsyx"
        __upper_cases = __letter_cases.upper()
        __numbers = "".join(map(str, range(3, 10)))
        __init_chars = ''.join((__letter_cases, __upper_cases, __numbers))
        __captcha_code = ""

        def __init__(self, mode="RGB",width=100, height=30, bgcolor=(200,200,25)):
                """
                :param mode: 默认是RGB颜色
                :param width: 验证码的默认宽度100
                :param height: 验证码的默认高度100
                :param bgcolor: 验证码的背景颜色
                """
                self.width = width
                self.height = height
                self.bgcolor = bgcolor
                self.instanceImage = Image.new(mode,(width,height),self.bgcolor) #实例化画面对象
                self.draw =ImageDraw.Draw(self.instanceImage) # 创建画笔
                self.Font = ""
                self.FontColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        def image_point(self):

                for i in range(0, 100):
                        xy = (random.randrange(0, self.width), random.randrange(0, self.height))
                        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
                        self.draw.point(xy, fill=fill)

        def captcha_code(self, Places= 4):

                for index in range(0, Places):

                                self.__captcha_code += str(self.__letter_cases[random.randint(0,len(self.__letter_cases)-1)])

                return self.__captcha_code

        def set_font(self, font_dir=None, font_size=25):
                """
                :param font_dir:
                :param font_size:

                :return:
                """
                font_dir = os.path.dirname(__file__)
                self.Font = ImageFont.truetype(font_dir+"/font/AldotheApache.ttf", font_size)
                return self.Font

        def set_captcha_text(self, coord=(), captcha_code="", fonts=None):
                """
                :param coord:
                :param captcha_code:
                :param fonts:
                :return:
                """
                captcha_code = " ".join(captcha_code)

                self.draw.text(xy=coord, text=captcha_code, font=fonts)



