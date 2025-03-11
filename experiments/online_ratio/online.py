import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

# 读取Excel文件
df = pd.read_excel('online.xlsx', header=None)

# 生成时间序列
start_time = pd.Timestamp('15:30')  # 开始时间
end_time = pd.Timestamp('13:30') + pd.Timedelta(days=1)  # 结束时间
time_range = pd.date_range(start=start_time, end=end_time, periods=len(df))

# 设置字体为Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 创建图表
plt.figure(figsize=(17.6/2.54, 13.2/2.54))
ax = plt.gca()
plt.plot(time_range, df[0], label='gzip', color='#383838')
plt.plot(time_range, df[1], label='Co4U', color='#D4352D')

# 设置图表标签
plt.xlabel('Time', fontsize=30)
plt.ylabel('Compression Rate', fontsize=30)

# 设置纵坐标显示百分号
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=0))

# 设置时间格式为小时和分钟
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# 设置横坐标刻度间隔为 5 小时
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=5))

# 添加图例
plt.legend(fontsize=28, loc='best')

# 调整刻度字体
plt.tick_params(axis='both', labelsize=30)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 直接控制坐标轴的位置和大小
ax.set_position([0.21, 0.2, 0.74, 0.75])

# 导出为PDF
plt.savefig('compression_rate_chart.pdf', bbox_inches='tight', dpi=1200)

# 显示图表
plt.show()