===============================
Data healer
===============================

A flasky app to categorize unlabeled datasets.


Why?
----

In machine learning world, sometimes you need to categorize an unlabeled dataset. Probably yo have obtained
data from a third party and in most cases the dataset is big and you try to categorize it using an unsupervised
learning algorithm such as `Latent Dirichlet Allocation <https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation/>`_,
`KMeans <https://en.wikipedia.org/wiki/K-means_clustering/>`_, `DBSCAN <https://en.wikipedia.org/wiki/DBSCAN/>`_, ...
However, depending on the nature of your data, get a good categorization with these algorithms is really hard and you
need that a human supervise the categorization. You can't infer a good classifier without a good labeled dataset.

With this purpose we have developed **data-healer**. A simple web application that helps you to label your datasets with
a fast and friendly interface. You just have to define some configs and give it a CSV input and start to categorize.
Each new categorization is registered in a new CSV with the same shape as the input one and an extra category column.

Finally, if you have tried first to infer the category with an unsupervised learning algorithm you can specify this
inferred column as a default option to speed up the category selection process.


Installation
------------

