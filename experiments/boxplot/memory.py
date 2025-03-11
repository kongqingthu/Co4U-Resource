import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# 读取 CSV 文件
data = pd.read_csv('data_percentage.csv')

# 处理空值，删除包含空值的行
data = data.dropna()

# 确保数据有四列
assert data.shape[1] == 4, "CSV 文件应包含四列数据"

# 设置字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# 线条颜色设置
lw = 1.8
line_colors = ["#fbce6a", "#383838", "#5ca7c7", "#d4352d"]  # 线条颜色（中位线、须线、边框）
box_colors = ["#fbce6a", "#383838", "#5ca7c7", "#d4352d"]   # 箱体填充颜色

# 自定义横轴标签
custom_labels = ["Brotli", "Gzip", "Zstd", "Co4U"]

# 创建图表
plt.figure(figsize=(17.6/2.54, 13.2/2.54))
ax = plt.gca()

# 使用 matplotlib 的 boxplot 函数绘制箱型图
bp = ax.boxplot(data.values, patch_artist=True, showfliers=False)

# 设置每个箱型图的颜色和线宽
n = len(custom_labels)
for i in range(n):
    # 箱体填充颜色
    bp['boxes'][i].set_facecolor(box_colors[i])
    # 箱体边框颜色及线宽
    bp['boxes'][i].set_edgecolor(line_colors[i])
    bp['boxes'][i].set_linewidth(lw)
    # 中位线颜色及线宽
    bp['medians'][i].set_color(line_colors[i])
    bp['medians'][i].set_linewidth(lw)
    # 须线颜色及线宽
    for whisker in bp['whiskers'][2*i:2*i+2]:
        whisker.set_color(line_colors[i])
        whisker.set_linewidth(lw)
    # 帽线颜色及线宽
    for cap in bp['caps'][2*i:2*i+2]:
        cap.set_color(line_colors[i])
        cap.set_linewidth(lw)

# 设置坐标轴标签和网格
plt.ylabel('Memory Usage (%)', fontsize=30)
plt.xticks(ticks=range(1, n+1), labels=custom_labels, fontsize=30)
plt.yticks(fontsize=30)
plt.grid(True)

# 直接控制坐标轴的位置和大小
ax.set_position([0.18, 0.2, 0.77, 0.75])

# 导出为PDF
plt.savefig('memory_boxplot.pdf', bbox_inches='tight', dpi=1200)

# 显示图表
plt.show()
