import sys
import itertools
import unidecode as ud
import pandas as pd
from collections import Counter
pd.set_option('display.max_colwidth', 0)

remove_duplicates = lambda x: ''.join(ch for ch, _ in itertools.groupby(x))

def get(path):
  df = pd.read_csv(path)
  df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
  df.rename(columns={df.columns[0]: 'index'}, inplace=True)
  df.drop(columns=['index'], inplace=True)
  return df

# Read data
submissions = get('data/cool_mini_or_not_submissions.csv')
comments = get('data/cool_mini_or_not_comments.csv')

submissions.head()
comments.head()

results = Counter()
comments['comment']\
  .str.lower()\
  .apply(ud.unidecode)\
  .replace('[^a-zA-Z0-9]', ' ',regex=True)\
  .apply(remove_duplicates) \
  .str.split()\
  .apply(results.update)

print(results)


# Exit
sys.exit()

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


