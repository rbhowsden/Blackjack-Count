import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


card_data = pd.read_parquet("blackjack_30m.parquet.gzip")

card_data["10"] = card_data["10"] + card_data["J"] + card_data["Q"] + card_data["K"]
card_data = card_data.drop(columns=['J', 'Q', 'K'])
card_data["card_total"] = card_data.iloc[:, :-2].sum(axis=1)
X = card_data[['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']]
y = card_data['outcome']

#for card in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
    #card_data[card+"_slope"] = card_data['card_total']*card_data[card]
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

card_reg = LinearRegression()
card_reg.fit(X, y)

print(card_reg.intercept_)
print(card_reg.coef_)

card_data['running_count'] = card_reg.predict(X) - card_reg.intercept_
card_data['interaction'] = card_data['card_total']*card_data['running_count']
card_data['predict'] = card_reg.predict(X)
card_data['residual'] = abs(card_data['outcome'] - card_data['predict'])
card_data['count_bucket'] = card_data['running_count']//.0025

X = card_data[['interaction']]

card_reg_2 = LinearRegression()
card_reg_2.fit(X, y)

print(card_reg_2.intercept_)
print(card_reg_2.coef_)
