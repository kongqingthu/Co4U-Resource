# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd

# def process_data(df1, df2, chunk_size=10000):
#     """处理数据，计算每chunk_size行的平均值"""
#     # 首先对两个数据框按文件名排序
#     df1 = df1.sort_values('File')
#     df2 = df2.sort_values('File')
    
#     # 确保两个文件的顺序一致
#     if not (df1['File'] == df2['File']).all():
#         raise ValueError("Files in both CSV files don't match after sorting!")
    
#     # 处理第一个文件的数据，移除百分号并转换为浮点数
#     data1 = {
#         'zstd': pd.to_numeric(df1['zstd'].str.rstrip('%'), errors='coerce'),
#         'brotli': pd.to_numeric(df1['brotli'].str.rstrip('%'), errors='coerce'),
#         'gzip': pd.to_numeric(df1['gzip'].str.rstrip('%'), errors='coerce'),
#         'zstd_dict': pd.to_numeric(df1['zstd_dict'].str.rstrip('%'), errors='coerce')
#     }
    
#     # 第二个文件的压缩率已经是小数，直接使用
#     compression_ratio = df2['Compression Ratio'].values * 100  # 转换为百分比
    
#     # 计算每chunk_size行的平均值
#     n_chunks = len(df1) // chunk_size + (1 if len(df1) % chunk_size != 0 else 0)
#     processed_data = {
#         'zstd': [],
#         'brotli': [],
#         'gzip': [],
#         'Co4U (original)': [],  # renamed from zstd_dict
#         'Co4U (update)': []     # from compression ratio
#     }
    
#     for i in range(n_chunks):
#         start_idx = i * chunk_size
#         end_idx = min((i + 1) * chunk_size, len(df1))
        
#         # 计算每个指标的平均值
#         processed_data['zstd'].append(np.mean(data1['zstd'][start_idx:end_idx]))
#         processed_data['brotli'].append(np.mean(data1['brotli'][start_idx:end_idx]))
#         processed_data['gzip'].append(np.mean(data1['gzip'][start_idx:end_idx]))
#         processed_data['Co4U (original)'].append(np.mean(data1['zstd_dict'][start_idx:end_idx]))
#         processed_data['Co4U (update)'].append(np.mean(compression_ratio[start_idx:end_idx]))
    
#     return processed_data, n_chunks

# def create_plot(file1, file2, output_file='compression_ratio.pdf'):
#     # 设置字体
#     plt.rcParams['font.family'] = 'Times New Roman'
#     plt.rcParams['font.size'] = 21
    
#     # 读取CSV文件
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)
    
#     # 打印排序前的前几行，用于调试
#     print("Before sorting - First few rows of first file:")
#     print(df1.head())
#     print("\nBefore sorting - First few rows of second file:")
#     print(df2.head())
    
#     # 处理数据
#     processed_data, n_chunks = process_data(df1, df2)
    
#     # 创建图形
#     plt.figure(figsize=(20, 11))
    
#     # 定义颜色映射
#     colors = {
#         'zstd': '#1f77b4',      # 蓝色
#         'brotli': '#ff7f0e',    # 橙色
#         'gzip': '#2ca02c',      # 绿色
#         'Co4U (original)': '#d62728',  # 红色
#         'Co4U (update)': '#9467bd'     # 紫色
#     }
    
#     # 创建x轴数据
#     x = np.arange(n_chunks)
    
#     # 绘制所有曲线
#     for label, color in colors.items():
#         plt.plot(x, processed_data[label], 
#                 label=label, 
#                 linewidth=3, 
#                 color=color)
    
#     # 设置图表属性
#     plt.xlabel('Message Number (10k)', fontsize=37.5, labelpad=10)
#     plt.ylabel('Compression Ratio (%)', fontsize=37.5, labelpad=10)
    
#     # 设置图例
#     plt.legend(loc='center left',
#               bbox_to_anchor=(1.02, 0.5),
#               frameon=True,
#               framealpha=0.9,
#               fontsize=25.5,
#               title='Compression Methods',
#               title_fontsize=25.5)
    
#     # 设置刻度
#     plt.xticks(fontsize=32)
#     plt.yticks(np.arange(30, 80, 10), fontsize=32)
    
#     # 添加网格
#     plt.grid(True, linestyle='--', alpha=0.7)
    
#     # 设置坐标轴范围
#     plt.xlim(0, n_chunks-1)
    
#     # 调整布局
#     plt.tight_layout()
    
#     # 保存图片
#     plt.savefig(output_file, format='pdf', dpi=300, bbox_inches='tight')
#     plt.close()

# # 使用示例
# create_plot('multi_folder_ratio_3.csv', 'compression_results_greedy_all_3.csv')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

def custom_sort_key(file_name):
    """ 根据文件夹和文件名进行自定义排序 """
    folder_order = {
        "ct": 1, "st": 2, "creative-ups_hdr": 3, "stable-ups_hdr": 4,
        "ct2": 5, "st2": 6, "ct3": 7, "st3": 8
    }
    
    folder_match = re.match(r'([^/]+)/(\d+)\.log', file_name)
    if not folder_match:
        return (999, 999999)  # 未匹配的排到最后
    
    folder, file_num = folder_match.groups()
    folder_rank = folder_order.get(folder, 999)  # 未知文件夹排在最后
    return (folder_rank, int(file_num))  # 文件按数字排序

def process_data(df1, df2, chunk_size=5000):
    """处理数据，计算每chunk_size行的平均值，并对齐文件列表"""
    df1 = df1.sort_values('File', key=lambda x: x.map(custom_sort_key))
    df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

    # 通过 merge 只保留两个数据框都包含的文件
    df_merged = pd.merge(df1, df2[['File']], on='File', how='inner')
    df2 = pd.merge(df2, df1[['File']], on='File', how='inner')

    # 再次排序，确保一致
    df_merged = df_merged.sort_values('File', key=lambda x: x.map(custom_sort_key))
    df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

    # 处理数据
    data1 = {
        'zstd': pd.to_numeric(df_merged['zstd'].str.rstrip('%'), errors='coerce'),
        'brotli': pd.to_numeric(df_merged['brotli'].str.rstrip('%'), errors='coerce'),
        'gzip': pd.to_numeric(df_merged['gzip'].str.rstrip('%'), errors='coerce'),
        #'zstd_dict': pd.to_numeric(df_merged['zstd_dict'].str.rstrip('%'), errors='coerce')
    }

    compression_ratio = df2['Compression Ratio'].values * 100  
    n_chunks = len(df_merged) // chunk_size + (1 if len(df_merged) % chunk_size != 0 else 0)
    # processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U (original)', 'Co4U (update)']}
    processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U']}

    for i in range(n_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(df_merged))
        processed_data['zstd'].append(np.mean(data1['zstd'][start_idx:end_idx]))
        processed_data['brotli'].append(np.mean(data1['brotli'][start_idx:end_idx]))
        processed_data['gzip'].append(np.mean(data1['gzip'][start_idx:end_idx]))
        #processed_data['Co4U (original)'].append(np.mean(data1['zstd_dict'][start_idx:end_idx]))
        processed_data['Co4U'].append(np.mean(compression_ratio[start_idx:end_idx]))

    return processed_data, n_chunks


def create_plot(file1, file2, output_file='compression_ratio.pdf'):
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 21
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    print("Before sorting - First few rows of first file:")
    print(df1.head())
    print("\nBefore sorting - First few rows of second file:")
    print(df2.head())
    
    processed_data, n_chunks = process_data(df1, df2)
    
    plt.figure(figsize=(20, 11))
    colors = {
        'zstd': '#1f77b4', 'brotli': '#ff7f0e', 'gzip': '#2ca02c',
        'Co4U': '#d62728'
    }#'Co4U ':  '#9467bd''#d62728',
    x = np.arange(n_chunks)
    
    for label, color in colors.items():
        plt.plot(x, processed_data[label], label=label, linewidth=3, color=color)
    
    plt.xlabel('Message Number (5k)', fontsize=37.5, labelpad=10)
    plt.ylabel('Compression Ratio (%)', fontsize=37.5, labelpad=10)
    plt.legend(loc='center left', bbox_to_anchor=(0.79, 0.83), frameon=True,
              framealpha=0.9, fontsize=25.5, title='Compression Methods',
              title_fontsize=25.5)
    plt.xticks(fontsize=32)
    plt.yticks(np.arange(0, 100, 10), fontsize=32)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, n_chunks-300)
    plt.tight_layout()
    plt.savefig(output_file, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()

# 使用示例
create_plot('multi_folder_ratio_4.csv', 'compression_results_greedy_all_4.csv')