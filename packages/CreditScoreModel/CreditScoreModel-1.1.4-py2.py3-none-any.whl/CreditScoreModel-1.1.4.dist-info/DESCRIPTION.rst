Project description
===================

CreditScoreModel
----------------

Installation
------------

::

    pip install CreditScoreModel

Basic Usage
-----------

::

    from CreditScoreModel.LogisticScoreCard import logistic_score_card #导入包

    ls=logistic_score_card() #初始化参数

    ls.fit(data) #模型训练

    ls.score(data) #检测模型结果

    ls.predict_score_proba(data) #预测用户分数和概率

    ls.score_card #制作好的评分卡


