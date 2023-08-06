# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from PIL import Image, ImageDraw, ImageFont
from ybc_exception import *
import sys
from curses import ascii


__CHINESE_FONT = '/usr/share/fonts/truetype/dejavu/fonts/NotoSansCJK-Bold.ttc'
__SYMBOL_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

# 小图标宽度，默认为 30 像素
__RESIZE_IMAGE_WIDTH = 30

# 生成新图片的宽度
__NEW_IMAGE_WIDTH = 500

# 字号
__FONT_SIZE = 40

# 输出在 canvas 区的行距
__LINE_HEIGHT = int(1.2 * __FONT_SIZE)


def word2emoji(word='', char=''):
    """
    功能：输入字和符号，在输出区打印出字符画。

    参数 word: 需要打印的字
    参数 char: 组成字的符号
    返回：无。
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(word, str):
        error_flag = -1
        error_msg += "'word'"
    if not isinstance(char, str):
        if error_flag == -1:
            error_msg += "、'char'"
        else:
            error_flag = -1
            error_msg += "'char'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if len(char) != 1:
        return -1

    if not word:
        error_flag = -1
        error_msg += "'word'"
    if not char:
        if error_flag == -1:
            error_msg += "、'char'"
        else:
            error_flag = -1
            error_msg += "'char'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        res_img = _text2image(word)
        txt = _image_to_string(res_img, char, width=__RESIZE_IMAGE_WIDTH, create_image=False)
        print(txt)
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_emoji')


def word2image(word='', char='', filename='word2image.jpg'):
    """
    功能：输入字和符号，在画板上画出字符画，可右键保存为图片。

    参数 word: 需要打印的字，
    参数 char: 组成字的符号，
    可选参数 filename: 保存后的文件名称，
    返回：None
    """
    error_flag = 1
    error_msg = ""
    if not isinstance(word, str):
        error_flag = -1
        error_msg += "'word'"
    if not isinstance(char, str):
        if error_flag == -1:
            error_msg += "、'char'"
        else:
            error_flag = -1
            error_msg += "'char'"
    if error_flag == -1:
        raise ParameterTypeError(sys._getframe().f_code.co_name, error_msg)

    if len(char) != 1:
        return -1

    if not word:
        error_flag = -1
        error_msg += "'word'"
    if not char:
        if error_flag == -1:
            error_msg += "、'char'"
        else:
            error_flag = -1
            error_msg += "'char'"
    if error_flag == -1:
        raise ParameterValueError(sys._getframe().f_code.co_name, error_msg)

    try:
        # 白底黑字图片
        transfer_img = _text2image(word)
        text = _image_to_string(transfer_img, char, width=__RESIZE_IMAGE_WIDTH, create_image=True)

        # 中文字符或全角字符，用 __CHINESE_FONT 字体绘图,其他字符用 __SYMBOL_FONT
        if _is_chinese(char):
            font_file_path = __CHINESE_FONT
        else:
            font_file_path = __SYMBOL_FONT

        font = ImageFont.truetype(font_file_path, __FONT_SIZE)

        # 新图片的尺寸
        img_width = _get_image_size(text, font, char)[0]
        img_height = img_width * 1.0 / transfer_img.size[0] * transfer_img.size[1]

        # 文字颜色，黑色
        word_color = '#000000'
        # 背景颜色，白色
        bg_color = '#ffffff'

        img = Image.new('RGB', (round(img_width), round(img_height)), bg_color)
        draw = ImageDraw.Draw(img)

        draw.text((0, 0), text, word_color, font)
        # 对生成的图片进行缩放
        img_height = int(__NEW_IMAGE_WIDTH * 1.0 / img_width * img_height)
        img = img.resize((__NEW_IMAGE_WIDTH, img_height), Image.NEAREST)
        img.save(filename)

        return None
    except (ParameterValueError, ParameterTypeError) as e:
        raise e
    except Exception as e:
        raise InternalError(e, 'ybc_emoji')


# 得到文字图画的尺寸
def _get_image_size(text, font, char):
    page_height = 0
    max_width = 0
    lines = text.split("\n")
    if _is_chinese(char):
        for i in range(0, len(lines)):
            page_height += font.getsize(lines[i])[1]
            page_width = font.getsize(lines[i])[1] * len(lines[i])
            if page_width > max_width:
                max_width = page_width
    else:
        for i in range(0, len(lines)):
            page_height += font.getsize(lines[i])[1]
            page_width = font.getsize(lines[i])[0]
            if page_width > max_width:
                max_width = page_width

    return max_width, page_height


def _is_emoji(content):
    """
    功能： 判断是否原生 emoji 表情，搜狗输入法表情 ❤️ ✨ 等会判断为false。

    :param content: 需要判断的表情符号。
    :return: True/False
    """
    if not content:
        return False
    # Smileys
    if u"\U0001F600" <= content and content <= u"\U0001F64F":
        return True
    # People and Fantasy
    elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
        return True
    # Clothing and Accessories
    elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
        return True
    # Pale Emojis
    elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
        return True
    else:
        return False


# 判断一个是否为中文字符或者全角字符
def _is_chinese(char):
    if (char >= u'\u4e00' and char <= u'\u9fa5') or (char >= u'\u3000' and char <= u'\u303F') or (char >= u'\uFF00' and char <= u'\uFFEF'):
        return True
    else:
        return False


def _text2image(word):
    """
    @brief 将一个中文字符转为白底黑字图片
    @params word: 中文字
    @params fontpath: 字体文件的路径
    @return image
    """
    # 中文字符或全角字符，用 __CHINESE_FONT 字体绘图,其他字符用 __SYMBOL_FONT
    if _is_chinese(word):
        fontpath = __CHINESE_FONT
    else:
        fontpath = __SYMBOL_FONT

    font = ImageFont.truetype(fontpath, 500)
    page_width = 500

    # 设置图宽高
    oneword_height = 0
    oneword_endheightlist = []

    for oneword in word:
        oneword_addheight = font.getsize(oneword)[1]
        nextheight = oneword_height+oneword_addheight
        oneword_endheightlist.append(nextheight)
        oneword_height = nextheight

    page_height = oneword_endheightlist[-1]

    # 文字颜色，黑色
    word_color = '#000000'
    # 背景颜色，白色
    bg_color = '#ffffff'

    img = Image.new('RGB', (page_width, page_height), bg_color)
    draw = ImageDraw.Draw(img)

    # 竖向输出字符
    height = 0
    for eword in word:
        addheight = font.getsize(word)[1]
        draw.text((0, height), eword, word_color, font)
        nextheight = height+addheight
        height = nextheight
    return img


def _image_to_string(img, char, width=30, create_image=False):
    """
    @brief 将图片转化为字符串
    @params img: 待打印的白底黑字的图片
    @params char: 替换图片的字符
    @params width: 由于像素点转为打印字符占用屏幕宽度挺大的, 所以需要对图片进行相应缩小，默认宽度为 30，大小为 30*38 像素.
    @return string
    """
    # 中文字符或全角字符，windows 系统对应 1 全角空格
    if _is_chinese(char):
        ascii_char = [char, '　']

    # mac 系统下的 emoji 宽度对应 1 个英文空格，为防止重叠额外增加一个英文空格；Windows 的彩色 emoji 暂无法对齐整数倍空格
    elif _is_emoji(char):
        char += ' '
        ascii_char = [char, '  ']

    # ascii 字符，对应 1 个半角空格，为保证输出内容的美观，对字符复制 2 倍
    elif _isascii(char):
        char += char
        ascii_char = [char, '  ']

    # 其他字符，如 ❤, windows 系统对应 1 半角空格
    else:
        # 若打印到输出区，防止字符表情重叠需要加一个半角空格；若生成图片，为保证输出内容的美观，对字符复制 2 倍
        if not create_image:
            char += ' '
        else:
            char += char
        ascii_char = [char, '  ']

    return _do_image2string(img, width, ascii_char)


def _do_image2string(img, width, ascii_char):
    def select_ascii_char(r, g, b):
        """ 在灰度图像中，灰度值最高为 255，代表白色，最低为 0，代表黑色 """
        gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)  # 'RGB－灰度值'转换公式
        if gray == 255:
            return ascii_char[1]
        else:
            return ascii_char[0]

    txt = ""
    old_width, old_height = img.size
    # 根据原图比例进行缩放，长宽比约为 5 : 4
    height = int(width * 1.0 / old_width * old_height)
    img = img.resize((width, height), Image.NEAREST)
    # img.show()
    for h in range(height):
        for w in range(width):
            # 每个像素点替换为字符
            txt += select_ascii_char(*img.getpixel((w, h))[:3])
        txt += '\n'
    return txt


def _isascii(s):
    return all(ascii.isascii(c) for c in s)


if __name__ == '__main__':
    # word2emoji('辅', '小')
    # word2emoji('辅', 'a')
    # word2emoji('辅', '.')
    # word2emoji('辅', '✨')
    # word2emoji('辅', '😊')

    # word2image('辅', '小')
    # word2image('辅', 'a')
    word2emoji('辅', '我')
    # word2image('辅', '❤')
    # word2image('超级大', '😊')
