import os
import shutil
import json

import textwrap
import gspread

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
from num2words import num2words

import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

from flask import render_template, send_file, request

from app import app

# a simple page that says hello
@app.route('/', methods=['GET', 'POST'])
def index():
    print_error = False
    if request.method == 'POST':
        voucher_ids = request.form['voucher_ids'].upper()
        verticle = request.form['verticle']
        # app.logger.info(voucher_ids)
        # app.logger.info(verticle)
        voucher_ids_li = voucher_ids.split(',')
        if len(voucher_ids_li) > 0 and len(voucher_ids_li[0]) >=3:
            pdf_path = img_to_pdf(voucher_ids_li,verticle)
            return send_file(pdf_path, as_attachment=True)
        else:
            print_error = True
    return render_template('index.html', print_error=print_error)

def fetch_data(verticle):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.getcwd(),\
     'app','static', 'credential', 'access-control-307101-2fd1a550d586.json'), scope)
    gc = gspread.authorize(creds)
    if verticle == 'Nursery':
      sheet = gc.open_by_key('1v3LeMrBvI5hj9-UsR6NzIMvNYuE0YQ3RF2JM-ZaDeGY')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      print(data_df.head())
      return data_df
    elif verticle == 'FM-KA':
      sheet1 = gc.open_by_key('1Jxrp7FZslYsinf1ePX7MKINSeUL7uL03COSbJoBfRfI')
      cleaned_data1 = sheet1.worksheet("voucherDetails")
      all_records1 = cleaned_data1.get_all_records()
      data_df1 = pd.DataFrame.from_dict(all_records1)
      data_df1 = data_df1.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df1.head())
      return data_df1
    elif verticle == 'Central Office':
      sheet = gc.open_by_key('1QXaXTQF7iIpPiWVE4wovDbFuAHVYCS0NPVN6u1Eiwbs')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df.head())
      return data_df
    elif verticle == 'Yavatmal':
      sheet = gc.open_by_key('1kZ8jF4IHAaTWerqEOhKZIvkExjtOp1Oowo6j2NuijqE')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df.head())
      return data_df
    elif verticle == 'IAM':
      sheet = gc.open_by_key('1y5tpUUttFcNG4d3QWuo9m12ULsYsM2dCG_A9WWUoiAQ')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df.head())
      return data_df
    elif verticle == 'FM-TN':
      sheet = gc.open_by_key('1HCWI8gkxQBoJi8s0hg2XwhxxZ3TT33hGEnudppKrPSo')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df.head())
      return data_df
    else :
      sheet = gc.open_by_key('1Pb1iF81kD7yrsK0eRah1m-EuQThWbzeel6BGf8ufl_A')
      cleaned_data = sheet.worksheet("voucherDetails")
      all_records = cleaned_data.get_all_records()
      data_df = pd.DataFrame.from_dict(all_records)
      data_df = data_df.drop(['Incurred By', 'Budget Head', 'Budget Name', 'Budget Sub-Head',\
            	    'Category',	'Verticle',	'Project Role',\
                    'Payment Date - UTR/DD/Cheque No.'], 1)
      # print(data_df.head())
      return data_df


class ImageText(object):
    def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        x, y = xy
        if isinstance(text, str):
            text = text.encode().decode(self.encoding)
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, xy, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False):
        x, y = xy
        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]
        height = y
        for index, line in enumerate(lines):
            height += text_height
            if place == 'left':
                self.write_text((x, height), line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text((x, height), line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text((start_x, height), word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text((last_word_x, height), words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)

def img_to_pdf(voucher_ids,verticle):

    data_df = fetch_data(verticle)
    data_df = data_df[data_df['Voucher No.'].isin(voucher_ids)]
    pdf = FPDF()
    for index, row in data_df.iterrows():

        font = os.path.join(os.getcwd(), 'app', 'static','fonts', 'Avenir-Medium.ttf')
        if row['Nature of Voc.'] != 'Advance':
            draw = ImageText(os.path.join(os.getcwd(), 'app', 'static', 'images', 'journal_voucher.jpg'), background=(255, 255, 255, 200))
            (x, y) = (400, 400)
            prepared_by = row['Prepared By']
            color = 'rgb(0, 0, 0)' # black color
            draw.write_text_box((x, y), prepared_by,  font_filename=font,box_width=800,font_size=50, color=color)


            (x1,y1) = (620,500)
            head_of_account = row['Head of Account']
            color = 'rgb(0,0,0)'
            draw.write_text_box((x1, y1), head_of_account, box_width=800,  font_filename=font,
                               font_size=50, color=color)


            (x2,y2) = (630,630)
            head_of_advance = row['Head of Advance']
            color = 'rgb(0,0,0)'
            draw.write_text_box((x2, y2), head_of_advance,box_width=1100,  font_filename=font,
                               font_size=50, color=color)


            (x3,y3) = (400,730)
            project = row['Location']
            color = 'rgb(0,0,0)'
            draw.write_text_box((x3, y3), project,box_width=600,  font_filename=font,
                               font_size=50, color=color)

            (x4,y4) = (320,950)
            particulars = row['Description']
            color = 'rgb(0,0,0)'

            draw.write_text_box((x4,y4), particulars, box_width=1800, font_filename=font,
                               font_size=50, color=color)

            (x9,y9) = (1700,730)
            budgetCode = row['Budget Code']
            color = 'rgb(0,0,0)'

            draw.write_text_box((x9,y9), budgetCode, box_width=1200, font_filename=font,
                               font_size=50, color=color)


            (x5,y5) = (340,1300)
            money = str(row['Amount']) + '/-'

            draw.write_text_box((x5,y5), money, box_width=1000, font_filename=font,
                               font_size=50, color=color)

            (x6,y6) = (430,1450)
            money_words = num2words(row['Amount'],to='cardinal', lang='en_IN')
            if len(money_words)>35:
                money_words_p1 = textwrap.wrap(money_words, 35)[0]
                money_words_p2 = textwrap.wrap(money_words, 35)[1] + ' only'
            else:
                money_words_p1 = money_words + ' only'
                money_words_p2 = ' '

            draw.write_text_box((x6,y6), money_words_p1.capitalize(), box_width=1000, font_filename=font,
                               font_size=50, color=color)

            draw.write_text_box((340, 1570), money_words_p2.capitalize(), box_width=600, font_filename=font,
                               font_size=50, color=color)

            (x7,y7) = (2300,200)
            date = str(row['Voucher Date'])
            draw.write_text_box((x7,y7), date, box_width=400, font_filename=font,
                               font_size=50, color=color)

            (x8,y8) = (2350,970)
            money2 = money
            draw.write_text_box((x8,y8), money2, box_width=400, font_filename=font,
                               font_size=50, color=color)

            (x10,y10) = (1300,200)
            donorName = str(row['Donor Name'])
            draw.write_text_box((x10,y10), donorName, box_width=400, font_filename=font,
                               font_size=50, color=color)

            (x11,y11) = (1350,150)
            donorType = str(row['LC/FC'])
            draw.write_text_box((x11,y11), donorType, box_width=400, font_filename=font,
                               font_size=50, color=color)

            img_path = os.path.join(os.getcwd(), 'app', 'static', 'images', 'filled_images',\
             'blank_img_filled' + str(index) + '.jpg')
            draw.save(img_path)
            # imagelist is the list with all image filenames
            pdf.add_page()
            pdf.image(img_path,0,0,210,148)
        else :
            draw = ImageText(os.path.join(os.getcwd(), 'app', 'static', 'images', 'bank_Voucher.jpg'), background=(255, 255, 255, 200))
            (x, y) = (650, 410)
            head_of_Advance = row['Head of Advance']
            color = 'rgb(0, 0, 0)' # black color
            draw.write_text_box((x, y), head_of_Advance,  font_filename=font,box_width=800,font_size=50, color=color)

            (x3,y3) = (450,630)
            project = row['Location']
            color = 'rgb(0,0,0)'
            draw.write_text_box((x3, y3), project,box_width=600,  font_filename=font,
                               font_size=50, color=color)

            (x4,y4) = (320,850)
            particulars = row['Description']
            color = 'rgb(0,0,0)'

            draw.write_text_box((x4,y4), particulars, box_width=1200, font_filename=font,
                               font_size=50, color=color)

            (x9,y9) = (1700,630)
            budgetCode = row['Budget Code']
            color = 'rgb(0,0,0)'

            draw.write_text_box((x9,y9), budgetCode, box_width=1200, font_filename=font,
                               font_size=50, color=color)

            (x1,y1) = (1350,200)
            donorName = str(row['Donor Name'])
            draw.write_text_box((x1,y1), donorName, box_width=400, font_filename=font,
                               font_size=50, color=color)

            (x2,y2) = (1400,150)
            donorType = str(row['LC/FC'])
            draw.write_text_box((x2,y2), donorType, box_width=400, font_filename=font,
                               font_size=50, color=color)


            (x6,y6) = (430,1490)
            money_words = num2words(row['Amount'],to='cardinal', lang='en_IN')
            if len(money_words)>35:
                money_words_p1 = textwrap.wrap(money_words, 35)[0]
                money_words_p2 = textwrap.wrap(money_words, 35)[1] + ' only'
            else:
                money_words_p1 = money_words + ' only'
                money_words_p2 = ' '

            draw.write_text_box((x6,y6), money_words_p1.capitalize(), box_width=1000, font_filename=font,
                               font_size=50, color=color)

            draw.write_text_box((340, 1590), money_words_p2.capitalize(), box_width=600, font_filename=font,
                               font_size=50, color=color)

            (x7,y7) = (2300,220)
            date = str(row['Voucher Date'])
            draw.write_text_box((x7,y7), date, box_width=400, font_filename=font,
                               font_size=50, color=color)

            (x8,y8) = (2250,820)
            money2 = str(row['Amount']) + '/-'
            draw.write_text_box((x8,y8), money2, box_width=400, font_filename=font,
                               font_size=50, color=color)

            img_path = os.path.join(os.getcwd(), 'app', 'static', 'images', 'filled_images',\
             'blank_img_filled' + str(index) + '.jpg')
            draw.save(img_path)
            # imagelist is the list with all image filenames
            pdf.add_page()
            pdf.image(img_path,0,0,210,148)

    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'app', 'static', 'images', 'filled_images')):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), 'app', 'static', 'pdfs')):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    pdf_path = os.path.join(os.getcwd(), 'app', 'static', 'pdfs', verticle + ''.join(voucher_ids) + '.pdf')
    pdf.output(pdf_path, "F")
    return pdf_path
    # return send_file(os.path.join(os.getcwd(), 'app/static', 'pdfs', 'voucher_filled_pdf' + '.pdf'), as_attachment=True)
