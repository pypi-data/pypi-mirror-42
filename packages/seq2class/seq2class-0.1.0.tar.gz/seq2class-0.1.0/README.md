# seq2class

seq2class is a one stop solution for text classification. Text classification using lstm is made easy via seq2class package.
This package is build by harnesing the capabilities of  LSTM(Long short term Memory) model.

One can use it using below steps:

```
data = 'movies.csv'
labels = 'title'
text = 'genres'

s = Sequence2class()

X_train, X_test, y_train, y_test = s.train_test_split(data, labels, text)

trained_model = s.fit_train(X_train, y_train, 500, 50, 7789, 5, 4)

prediction = s.predict(trained_model, X_test, y_train, 4)

```

