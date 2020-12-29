import unidecode as ud
import pandas as pd
pd.set_option('display.max_colwidth', 0)

# Read data
submissions = pd.read_csv('data/cool_mini_or_not_submissions.csv')
comments = pd.read_csv('data/cool_mini_or_not_comments.csv')

submissions.rename(columns={submissions.columns[0]: 'index'}, inplace=True)
comments.rename(columns={comments.columns[0]: 'index'}, inplace=True)

submissions.drop(columns=['index'], inplace=True)
comments.drop(columns=['index'], inplace=True)

submissions.head()
comments.head()

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

for index, row in comments.iterrows():
    print(row['comment'])
    print(ud.unidecode(row['comment']))
    #print(ud.unidecode(row['comment']).lower().re.split())

