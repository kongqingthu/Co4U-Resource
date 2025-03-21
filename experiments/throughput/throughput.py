import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'

# 读取CSV文件
df1 = pd.read_csv('throughput_stats_sender1.csv')
df2 = pd.read_csv('new.csv')

# 获取时间戳列和吞吐量列
time1 = df1.iloc[:, 0]
time2 = df2.iloc[:, 0]
throughput1 = df1.iloc[:, 1]
throughput2 = df2.iloc[:, 1]

# 获取 sender2 的第一个时间戳
start_time_sender2 = time2.iloc[0]

# 将时间戳转换为相对时间，减去 sender2 的第一个时间戳
relative_time1 = time1 - start_time_sender2
relative_time2 = time2 - start_time_sender2

# 计算滑动平均
windowsize = 15
smoothed_throughput1 = throughput1.rolling(window=windowsize).mean()
smoothed_throughput2 = throughput2.rolling(window=windowsize).mean()

# 创建一个图形
plt.figure(figsize=(17.6/2.54, 13.2/2.54))
ax = plt.gca()

# 绘制第一个数据集（Sender 1）
plt.plot(relative_time1, smoothed_throughput1, label='Co4U', color='#D4352D')

# 绘制第二个数据集（Sender 2）
plt.plot(relative_time2, smoothed_throughput2, label='Original', color='#383838')

# 设置标签和标题
plt.xlabel('Time (s)', fontsize=30)
plt.ylabel('Throughput (Mbps)', fontsize=30)

# 设置坐标轴刻度
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlim(left=-100, right=4700)

# 添加图例
plt.legend(loc='best', fontsize=30)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 直接控制坐标轴的位置和大小
ax.set_position([0.17, 0.2, 0.78, 0.75])

# 导出为PDF
plt.savefig('throughput.pdf', bbox_inches='tight', dpi=1200)

# 显示图表
plt.show()
