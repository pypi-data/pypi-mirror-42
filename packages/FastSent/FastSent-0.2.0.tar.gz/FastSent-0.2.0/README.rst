FastSent is Sentiment Classification python library. It uses Sequential model for Sentiment classfication. FastSent is developed using GRU(Gated Recurrent Unit) model.

Requirement
------------

FastSent support Python 3.6 or newer.

Installation
------------

    pip install FastSent

Example
-------------

This package is being developed for sentiment classfication using Sequential model GRU(Gated Recurrent Unit).

	data = 'Sample.csv'
	labels = 'sentiment'
	text = 'content'

	f = FastSent()
	X_train, X_test, y_train, y_test = f.train_test_split(data, labels, text)
	trained_model = f.fit_train(X_train, y_train, 500, 50, 7789, 5, 4)
	prediction = f.predict(trained_model, X_test, y_train, 4)




where ``sample`` is a training file containing labels and text.

References
----------

DataSet Information
~~~~~~~~~~~~~~~~~~~

[1] Sample DataSet is being used for research purpose from  `*data.world* <https://data.world/crowdflower/sentiment-analysis-in-text>`.