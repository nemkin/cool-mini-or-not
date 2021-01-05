import sys
import os
import pandas as pd
import helper
import re
import traceback
from datetime import datetime as dt

from lxml import html
from lxml import etree

location = "/home/nemkin/Mount/drive/Wayback"
#location = "/home/nemkin/Mount/drive/Wget/www.coolminiornot.com"
index_file = "index.html"

submissions = []
ebay = []
comments = []

def strip(l):
  return list(map(lambda s: s.strip(), l))

def get_entries():
  global location
  dirs = os.listdir(location)
  entries = list(filter(lambda dir: dir.isnumeric(), dirs))
  return entries

def process_comments(file_path, entry_id, tree):
  global comments

  comment_rows = tree.xpath('//table[@class="comments_list"]/tbody/tr')

  for comment_row in comment_rows:
    [commenter_td, comment_text_td] = comment_row.xpath('td')

    [commenter_url, *_] = commenter_td.xpath('.//a/@href')

    [comment_id] = comment_text_td.xpath('.//td[@class="comment_header_left"]/b/text()')
    try:
      [vote] = comment_text_td.xpath('.//td[@class="comment_header_center"]/b/span/text()')
    except ValueError:
      vote = ''
    [comment_date] = comment_text_td.xpath('.//td[@class="comment_header_right"]/b/text()')
    comment_date_parsed = dt.strptime(comment_date, "%d %b %Y").strftime("%Y-%m-%d")

    comment = " ".join(strip(comment_text_td.xpath('text()')))
    comment_sanitized = re.sub(' {2,}', ' ', comment.replace('\n', ' '))

    _, commenter_user = commenter_url.split('?')

    [commenter_user_id, *_] = commenter_user.split('-')
    commenter_user_name = commenter_user[len(commenter_user_id)+1:]

    comment_columns = [
      entry_id, comment_id[1:], comment_date_parsed, commenter_user_id,
      commenter_user_name, vote, comment_sanitized]

    comments.append(strip(comment_columns))

def process_entry(entry_id):
  global location
  global index_file
  global submissions
  global ebay

  dir_path = f"{location}/{entry_id}"
  main_file_path = f"{dir_path}/{index_file}"

  try:
    with open(main_file_path, "r") as main_file:
      main_page = main_file.read()
  except IOError as e:
    print(f"IOError during opening main file path: {e}")
    print()
    return

  try:
    tree = html.fromstring(main_page)
  except:
    print(f"Can't get HTML tree for {entry_id} with page {main_page}")
    print()
    return

  boxes = tree.xpath('//div[@class="box"]')
  [artwork_info, _, submission, *_] = tree.xpath('//div[@class="box"]/div[@class="block"]')

  try:
    [entry_name] = artwork_info.xpath('b/u/text()')
  except Exception as e:
    print(f"Error during name parse: {e}")
    entry_name = ""
  entry_name = entry_name.replace(';', ',')

  [manufacturer, category] = artwork_info.xpath('b/text()')
  [user_id, _] = artwork_info.xpath('a[@class="userProfile"]/@uid')
  user_name = artwork_info.xpath('a[@class="userProfile"]/text()')[-1]

  [entry_date, vote_count, view_count] = artwork_info.xpath('span[@class="socialLink"]/b/text()')
  entry_date_parsed = dt.strptime(entry_date, "%d %b %Y").strftime("%Y-%m-%d")

  [vote_average] = artwork_info.xpath('span[@class="socialLink"]/b/font/text()')

  [entry_image_url] = submission.xpath('//img[@id="artworkIMG"]/@src')

  entry_image = entry_image_url

  ebay_forms = submission.xpath('.//form')
  if len(ebay_forms) == 1:
    [ ebay_form ] = ebay_forms
    [ ebay_id ] = ebay_form.xpath('./a/text()')
    ebay_data = ebay_form.xpath('./b/text()')

    if len(ebay_data) == 4:
      [ ebay_current_price, ebay_first_bid, ebay_number_of_bids, ebay_end_date ] = ebay_data
      ebay_end_date_parsed = dt.strptime(ebay_end_date, "%Y- %m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    else:
      [ ebay_current_price, ebay_first_bid, ebay_number_of_bids, ebay_end_date ] = [""]*4
      ebay_end_date_parsed = ""

    ebay_columns = [ entry_id, ebay_id, ebay_current_price, ebay_first_bid, ebay_number_of_bids, ebay_end_date_parsed ]
    ebay.append(strip(ebay_columns))

  else:
    if 1 < len(ebay_forms):
      print(entry_id, " multiple ebay forms?")

  columns = [
    entry_id, entry_date_parsed, entry_name, entry_image, user_id, user_name, manufacturer, category,
    view_count, vote_count, vote_average
  ]

  submissions.append(strip(columns))
  process_comments(f"{entry_id}/{index_file}", entry_id, tree)

  dir_contents = sorted(os.listdir(dir_path))
  for dir_content in dir_contents:
    sub_dir_path = f"{dir_path}/{dir_content}"
    if os.path.isdir(sub_dir_path):
      sub_file_path = f"{sub_dir_path}/{index_file}"
      try:
        with open(sub_file_path, "r") as sub_file:
          sub_page = sub_file.read()
      except IOError as e:
        print(f"IOError during subpage html file opening: {e}")
        print()
        continue
      sub_tree = html.fromstring(sub_page)
      process_comments(f"{entry_id}/{dir_content}/{index_file}", entry_id, sub_tree)

entries = get_entries()
results = []
bad_entries = open('../data/bad_entries.txt', 'a')

l = len(entries)
print(entries)
print(f"Total: {l}")
helper.printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
for i, entry in enumerate(entries):
  try:
    process_entry(entry)
  except :
    bad_entries.write(f"BADENTRY: {entry} ({i})")
    print()
    print()
    print(f"BADENTRY: {entry} ({i})")
    print()
    traceback.print_exc()
    print()
  helper.printProgressBar(i+1, l, prefix='Progress:', suffix=f"Current: {entry}", length=50)

bad_entries.close()

submissions_df = pd.DataFrame(
  data = submissions,
  columns = [
    "entry_id", "entry_date", "entry_name", "entry_image", "user_id", "user_name", "manufacturer", "category",
    "view_count", "vote_count", "vote_average"
  ])
ebay_df = pd.DataFrame(
  data = ebay,
  columns = [
    "entry_id", "ebay_id", "ebay_current_price", "ebay_first_bid", "ebay_number_of_bids", "ebay_end_date"
  ])
comments_df = pd.DataFrame(
  data = comments,
  columns = [
      "entry_id", "comment_id", "comment_date", "commenter_user_id",
      "commenter_user_name", "vote", "comment"
  ])

submissions_df.to_csv("../data/cool_mini_or_not_submissions.csv")
ebay_df.to_csv("../data/cool_mini_or_not_ebay.csv")
comments_df.to_csv("../data/cool_mini_or_not_comments.csv")

