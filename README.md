# Node-Diversity
The information about this repository is as follows.

## Citation
Fu, Y. H., Huang, C. Y., & Sun, C. T. (2015). Using global diversity and local topology features to identify influential network spreaders. Physica A: Statistical Mechanics and its Applications, 433, 344-355.

## Abstract
Identifying the most influential individuals spreading ideas, information, or infectious diseases is a topic receiving significant attention from network researchers, since such identification can assist or hinder information dissemination, product exposure, and contagious disease detection. Hub nodes, high betweenness nodes, high closeness nodes, and high -shell nodes have been identified as good initial spreaders. However, few efforts have been made to use node diversity within network structures to measure spreading ability. The two-step framework described in this paper uses a robust and reliable measure that combines global diversity and local features to identify the most influential network nodes. Results from a series of Susceptible–Infected–Recovered (SIR) epidemic simulations indicate that our proposed method performs well and stably in single initial spreader scenarios associated with various complex network datasets.

The url of the paper is https://doi.org/10.1016/j.physa.2015.03.042.

## Setting of the execution environment
In this paper, we used Python 3.4, NetworkX 1.9.1, Numpy 1.9.2 and Scipy 0.15.1 for programming. Also, for the IDE of Python, we recommend the PyCharm community version.

However, the Python 3.4 is no longer compatible for `Conda` to create the `env` environment. Therefore, you coulde add the mirror channel to `Conda` by using `conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/`. Then, you could use `conda create -n Python34 python=3.4 anaconda` to create the `Conda env` of Python3.4.

## Simple code usage
1. use `measure_node_attribute.py` to create `file\*.pickle`, e.g., `file\polblogs_gcc-attr.pickle`
2. use `network_attribute_scatter.py` to draw scatters of nodes' attributes, e.g., `image\network_attribute_scatter_net=polblogs_gcc.png`
3. use `experiment1.py` to run SIR simulations and draw plots, e.g., `network_propagation,net=polblogs_gcc,round=1000,t=50,topk=1,b=0.02,r=1.png` and `propagation_result,net=polblogs_gcc,round=1000,t=50,topk=1,b=0.02,r=1.txt`

## Notification
1. You are free to use the codes for educational purposes.
2. Our coding style may not as good as you expect, but it works.
3. We are glad to hear your improvements of the codes.
4. Any questions please contact yuhisnag.fu@gmail.com.

Best regards,
Yu-Hsiang Fu 20220103 updated.
