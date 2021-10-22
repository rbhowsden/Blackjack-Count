import pandas as pd
from sklearn.linear_model import LinearRegression

card_data = pd.read_parquet("blackjack.parquet.gzip")
card_data["10"] = card_data["10"] + card_data["J"] + card_data["Q"] + card_data["K"]
card_data = card_data.drop(columns=['J', 'Q', 'K'])

X = card_data[['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']]
y = card_data['outcome']

card_reg = LinearRegression()
card_reg.fit(X, y)

card_data["card_total"] = card_data.iloc[:, :-2].sum(axis=1)
card_data['running_count'] = card_reg.predict(X) - card_reg.intercept_
card_data['interaction'] = card_data['card_total']*card_data['running_count']

X = card_data[['interaction']]

card_reg_2 = LinearRegression()
card_reg_2.fit(X, y)
