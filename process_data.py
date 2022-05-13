import pandas as pd

df = pd.read_csv('./data/menu_data.csv', encoding='cp949')
categories = {
    category: '/'.join(category.split('.')) for category in df.category.unique()
}
df.category = df.category.apply(lambda x: categories[x])

df[['category']].drop_duplicates().to_csv('./data/categories.csv', index=False)
df[['menu','category']].drop_duplicates().to_csv('./data/foods.csv', index=False)

print('DONE: Processed menu_data.csv\'s categories.')