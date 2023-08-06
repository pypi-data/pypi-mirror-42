# FastSent

FastSent is Sentiment Classification python package. It uses Sequential model for Sentiment classfication.
FastSent is developed using GRU(Gated Recurrent Unit) model.


One can use it using below steps:


```
data = 'Sample.csv'
labels = 'sentiment'
text = 'content'

f = FastSent()

X_train, X_test, y_train, y_test = f.train_test_split(data, labels, text)

trained_model = f.fit_train(X_train, y_train, 500, 50, 7789, 5, 4)

prediction = f.predict(trained_model, X_test, y_train, 4)
```

Reference: Above data set have been taken from this website https://data.world/crowdflower/sentiment-analysis-in-text for research and experiment purpose.
