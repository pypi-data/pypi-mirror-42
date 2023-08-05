# KTBoost - A Python Package for Boosting

This Python package implements several boosting algorithms with different combinations of base learners, optimization algorithms, and loss functions.

## Description

Concerning **base learners**, KTboost includes:

* Trees 
* Reproducing kernel Hilbert space (RKHS) ridge regression functions (i.e., posterior means of Gaussian processes)
* A combination of the two (i.e., the KTBoost algorithm) 


Concerning the **optimization** step for finding the boosting updates, the package supports:

* Gradient descent
* Newton method (if applicable)
* A hybrid version of the two for trees as base learners


The package implements the following **loss functions**:

 * Continuous data ("regression"): quadratic loss (L2 loss), absolute error (L1 loss), Huber loss, quantile regression loss, Gamma regression loss, negative Gaussian log-likelihood with both the mean and the standard deviation as functions of features
* Count data ("regression"): Poisson regression loss
* (Unorderd) Categorical data ("classification"): logistic regression loss (log loss), exponential loss, cross entropy loss with softmax
* Mixed continuous-categorical data ("censored regression"): negative Tobit likelihood (i.e., the Grabit model)




## Installation

It can be **installed** using 
```
pip install -U KTBoost
```
and then loaded using 
```python
import KTBoost.KTBoost as KTBoost
```

## Usage and examples
The package is build as an extension of the scikit-learn implementation of boosting algorithms and its workflow is very similar to that of scikit-learn.

The two main classes are `KTBoost.BoostingClassifier` and `KTBoost.BoostingRegressor`. 

The following **code examples** show how the package can be used.


#### Define models, train models, make predictions
```python
import KTBoost.KTBoost as KTBoost

################################################
## Define model (see below for more examples) ##
################################################
## Standard tree-boosting for regression with quadratic loss and hybrid gradient-Newton updates as in Friedman (2001)
model = KTBoost.BoostingRegressor(loss='ls')

##################
## Train models ##
##################
model.fit(Xtrain,ytrain)

######################
## Make predictions ##
######################
model.predict(Xpred)
```

#### More examples of models
```python
#############################
## More examples of models ##
#############################
## Boosted Tobit model, i.e. Grabit model (Sigrist and Hirnschall, 2017), 
## with lower and upper limits at 0 and 100
model = KTBoost.BoostingRegressor(loss='tobit',yl=0,yu=100)
## KTBoost algorithm (combined kernel and tree boosting) for classification with Newton updates
model = KTBoost.BoostingClassifier(loss='deviance',base_learner='combined',
                                    update_step='newton',theta=1)
## Gradient boosting for classification with trees as base learners
model = KTBoost.BoostingClassifier(loss='deviance',update_step='gradient')
## Newton boosting for classification model with trees as base learners
model = KTBoost.BoostingClassifier(loss='deviance',update_step='newton')
## Hybrid gradient-Newton boosting (Friedman, 2001) for classification with 
## trees as base learners (this is the version that scikit-learn implements)
model = KTBoost.BoostingClassifier(loss='deviance',update_step='hybrid')
## Kernel boosting for regression with quadratic loss
model = KTBoost.BoostingRegressor(loss='ls',base_learner='kernel',theta=1)
## Kernel boosting with the Nystroem method and the range parameter theta chosen 
## as the average distance to the 100-nearest neighbors (of the Nystroem samples)
model = KTBoost.BoostingRegressor(loss='ls',base_learner='kernel',nystroem=True,
                                  n_components=1000,theta=None,n_neighbors=100)
## Regression model where both the mean and the standard deviation depend 
## on the covariates / features
model = KTBoost.BoostingRegressor(loss='msr')
```

#### Feature importances and partial dependence plots
```python
#########################
## Feature importances ## (only defined for trees as base learners)
#########################
Xtrain=np.random.rand(1000,10)
ytrain=2*Xtrain[:,0]+2*Xtrain[:,1]+np.random.rand(1000)

model = KTBoost.BoostingRegressor()
model.fit(Xtrain,ytrain)
## Extract feature importances calculated as described in Friedman (2001)
feat_imp = model.feature_importances_

## Alternatively, plot feature importances directly
KTBoost.plot_feature_importances(model=model,feature_names=feature_names,maxFeat=10)

##############################
## Partial dependence plots ## (currently only implemented for trees as base learners)
##############################
from KTBoost.partial_dependence import plot_partial_dependence
import matplotlib.pyplot as plt
features = [0,1,2,3,4,5]
fig, axs = plot_partial_dependence(model,Xtrain,features,percentiles=(0,1),figsize=(8,6))
plt.subplots_adjust(top=0.9)
fig.suptitle('Partial dependence plots')

## Alternatively, get partial dependencies in numerical form
from KTBoost.partial_dependence import partial_dependence
kwargs = dict(X=Xtrain, percentiles=(0, 1))
partial_dependence(model,[0],**kwargs)
```

## Author
Fabio Sigrist

## References

* Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. The annals of statistics, 1189-1232.
* Sigrist, F., & Hirnschall, C. (2017). Grabit: Gradient Tree Boosted Tobit Models for Default Prediction. arXiv preprint arXiv:1711.08695.
* Sigrist, F. (2018). Gradient and Newton Boosting for Classification and Regression. arXiv preprint arXiv:1808.03064.
* Sigrist, F. (2019). KTBoost: Combined Kernel and Tree Boosting. arXiv preprint arXiv:1902.03999.