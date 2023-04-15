topic : Association Rules Mining
coder : Wenzhuo Ma
email : mawenzhuogorgeous@gmail.com
date : 2023-04-15
language : python
version : 3.7.16
third-party library : pandas, os, prettytable, tqdm, itertools, matplotlib
details : From the keywords of 16,071 articles, the keyword combination with correlation was found, and the validity of the correlation was evaluated
file structure:
    code:代码文件夹
        associate_rules.py:关联规则挖掘代码
        analysis.py:分析评价代码
    result:结果文件夹
        associate_rules_prune_s0.025_c0.85.log:支持度阈值为0.025置信度阈值为0.85的过程和结果
        associate_rules_prune.log:加上剪枝的运过程和结果
        associate_rules.log:没有剪枝的运行过程和结果
        analysis.png:分析三维图
        analysis.log:分析运行过程和结果
    readme.txt
    分析报告.pdf
    步骤流程图.jpg
