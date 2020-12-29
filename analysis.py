import sys
import itertools
import unidecode as ud
import numpy as np
import pandas as pd
from collections import Counter
pd.set_option('display.max_colwidth', 0)

remove_duplicates = lambda x: ''.join(ch for ch, _ in itertools.groupby(x))

def read(path):
  df = pd.read_csv(path)
  df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
  df.rename(columns={df.columns[0]: 'index'}, inplace=True)
  df.drop(columns=['index'], inplace=True)
  return df

def eval(df):
  print(df.dtypes)
  print('-')
  print(df.head())

  # print('-')
  # for col in df.columns:
  #   print(col)
  #   print(df[col].unique())

def most_common_words(df):
  results = Counter()
  df['comment']\
    .str.lower()\
    .apply(ud.unidecode)\
    .replace('[^a-zA-Z0-9]', ' ',regex=True)\
    .str.split()\
    .apply(results.update)
  return results

#    .apply(remove_duplicates) \

# Read data
submissions = read('data/cool_mini_or_not_submissions.csv')
comments = read('data/cool_mini_or_not_comments.csv')

submissions['entry_date'] = pd.to_datetime(submissions['entry_date'], errors='coerce')
comments["vote"] = pd.to_numeric(comments['vote'], errors='coerce').fillna(0).astype(np.int64)

print()
print('Submissions')
print('---------')
eval(submissions)

print()
print('Comments')
print('---------')
eval(comments)

counts = submissions['entry_date']\
  .groupby([submissions['entry_date'].dt.month, \
            submissions['entry_date'].dt.day]).count()
plot = counts.plot(kind='bar')
plot.figure.set_size_inches(60, 30)
plot.figure.savefig('plot.png', dpi=200)

# Exit
sys.exit()

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


for index, row in comments.iterrows():
  print(index)
  print(row['comment'])
  print(ud.unidecode(row['comment']))
  #print(ud.unidecode(row['comment']).lower().re.split())

joined = submissions \
  .set_index('entry_id') \
  .join(comments.set_index('entry_id'), lsuffix='_submissions', rsuffix='_comments')

# Értékelések eloszlása a beküldéseken:
submissions.hist(column='vote_average', bins=10)

# Az adott értékelésű beküldéseket milyen gyakran nézték meg:
submissions.plot.scatter(x='vote_average', y='view_count')

# Az adott értékelésű beküldésekre milyen konkrét egyedi értékelések jöttek:
# joined.plot.scatter(x='vote_average', y='vote') # Float is bad

# Beküldések darabszáma kategóriánként:
submissions.groupby('category').count().plot.bar()


