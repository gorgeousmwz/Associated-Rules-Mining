import associate_rules as ar
import prettytable as pt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

record=[]
index=0
support_threhold=0.005
while support_threhold<0.03:
    confidence_threshlod=0.6
    while confidence_threshlod<0.9:
        index+=1
        print(f'================================【support_threshold:{support_threhold},confidence_threshold:{confidence_threshlod}】================================')
        useful_rules,tb=ar.get_associate_rules('/home/ubuntu/mwz/Spatio-temporal_data_mining_and_analysis/data',['Author Keywords','Keywords Plus'],support_threhold,confidence_threshlod)
        record.append([index,support_threhold,confidence_threshlod,len(useful_rules)])
        confidence_threshlod+=0.05
    support_threhold+=0.005
tb=pt.PrettyTable()
tb.field_names=['index','support_threshold','confidence_threshold','number of rules']
for item in record:
    tb.add_row(item)
print(f'====================================【All In All】====================================')
print(tb)

# 绘图
x = [r[1] for r in record]
y = [r[2] for r in record]
z = [r[3] for r in record]
# 创建三维图形对象
fig = plt.figure()
ax = Axes3D(fig)
# 绘制三维图形
ax.scatter(x, y, z)
# 设置坐标轴标签
ax.set_xlabel('support_threshold')
ax.set_ylabel('confidence_support')
ax.set_zlabel('long')
# 保存图形
plt.savefig('Spatio-temporal_data_mining_and_analysis/work1/analysis.png')