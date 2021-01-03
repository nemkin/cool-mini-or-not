import sys
import itertools
import unidecode as ud
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
pd.set_option('display.max_colwidth', 0)

def read(path):
  df = pd.read_csv(path)
  df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
  df.rename(columns={df.columns[0]: 'index'}, inplace=True)
  df.drop(columns=['index'], inplace=True)
  return df

def eval(name, df):
  print()
  print(name)
  print('---------')
  print(df.dtypes)
  print('-')
  print(df.head())
  print('-')
  print(df.describe())
  # print('-')
  # for col in df.columns:
  #   print(col)
  #   print(df[col].unique())

submissions = read('data/cool_mini_or_not_submissions.csv')
comments = read('data/cool_mini_or_not_comments.csv')

submissions['entry_date'] = pd.to_datetime(submissions['entry_date'], errors='coerce')
comments['comment_date'] = pd.to_datetime(comments['comment_date'], errors='coerce')
comments['vote'] = pd.to_numeric(comments['vote'], errors='coerce').fillna(0).astype(np.int64)

eval('Submissions', submissions)
eval('Comments', comments)

joined = submissions \
  .set_index('entry_id') \
  .join(comments.set_index('entry_id'), lsuffix='_submissions', rsuffix='_comments')

# Begin

def most_common_words(df):
  results = Counter()
  remove_duplicates = lambda x: ''.join(ch for ch, _ in itertools.groupby(x))
  df['comment'] \
    .str.lower() \
    .apply(ud.unidecode) \
    .replace('[^a-zA-Z0-9]', ' ', regex=True) \
    .str.split() \
    .apply(results.update)
  return results
#    .apply(remove_duplicates) \

def plot_submission_counts_per_day_of_the_year():
  global submissions
  submission_counts = submissions['entry_date']\
    .groupby([submissions['entry_date'].dt.month, \
              submissions['entry_date'].dt.day]).count()
  plot = submission_counts.plot(kind='bar')
  plot.figure.set_size_inches(60, 30)
  plot.figure.savefig('results/submission_counts_per_day_of_the_year.png', dpi=200)

def other_plots():
  # Értékelések eloszlása a beküldéseken:
  submissions[['vote_average']].hist(column='vote_average', bins=10)
  plt.savefig('results/vote_average_histogram.png', dpi=200)
  # Az adott értékelésű beküldéseket milyen gyakran nézték meg:
  submissions.plot.scatter(x='vote_average', y='view_count')
  plt.savefig('results/vote_average_view_count_scatter.png', dpi=200)
  # Az adott értékelésű beküldésekre milyen konkrét egyedi értékelések jöttek:
  # joined.plot.scatter(x='vote_average', y='vote') # Float is bad
  # Beküldések darabszáma kategóriánként:
  submissions.groupby('category').count().plot.bar()

def eval_mcw():
  # Most common words
  mca = most_common_words(comments)
  mcg = most_common_words(comments.loc[comments['vote']>5])
  mcb = most_common_words(comments.loc[comments['vote']<6])
  print('---')
  print(mca)
  print('---')
  print(mcg)
  print('---')
  print(mcb)
  print('---')


table = pd.pivot_table( \
          comments, \
          values='vote', \
          index='commenter_user_name', \
          columns='entry_id', \
          aggfunc=max)
# table.to_csv('pivot.csv', index=False)
print(table)

corr_tab = table.corr()
table.to_csv('corr_pivot.csv', index=False)
print(corr_tab)

