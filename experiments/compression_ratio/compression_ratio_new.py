
# # import matplotlib.pyplot as plt
# # import numpy as np
# # import pandas as pd
# # import re

# # def custom_sort_key(file_name):
# #     """ 根据文件夹和文件名进行自定义排序 """
# #     folder_order = {
# #         "ct": 1, "st": 2, "creative-ups_hdr": 3, "stable-ups_hdr": 4,
# #         "ct2": 5, "st2": 6, "ct3": 7, "st3": 8
# #     }
    
# #     folder_match = re.match(r'([^/]+)/(\d+)\.log', file_name)
# #     if not folder_match:
# #         return (999, 999999)  # 未匹配的排到最后
    
# #     folder, file_num = folder_match.groups()
# #     folder_rank = folder_order.get(folder, 999)  # 未知文件夹排在最后
# #     return (folder_rank, int(file_num))  # 文件按数字排序

# # def process_data(df1, df2, chunk_size=10000):
# #     """处理数据，计算每chunk_size行的平均值，并对齐文件列表"""
# #     df1 = df1.sort_values('File', key=lambda x: x.map(custom_sort_key))
# #     df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

# #     # 通过 merge 只保留两个数据框都包含的文件
# #     df_merged = pd.merge(df1, df2[['File']], on='File', how='inner')
# #     df2 = pd.merge(df2, df1[['File']], on='File', how='inner')

# #     # 再次排序，确保一致
# #     df_merged = df_merged.sort_values('File', key=lambda x: x.map(custom_sort_key))
# #     df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

# #     # 处理数据
# #     data1 = {
# #         'zstd': pd.to_numeric(df_merged['zstd'].str.rstrip('%'), errors='coerce'),
# #         'brotli': pd.to_numeric(df_merged['brotli'].str.rstrip('%'), errors='coerce'),
# #         'gzip': pd.to_numeric(df_merged['gzip'].str.rstrip('%'), errors='coerce'),
# #         #'zstd_dict': pd.to_numeric(df_merged['zstd_dict'].str.rstrip('%'), errors='coerce')
# #     }

# #     compression_ratio = df2['Compression Ratio'].values * 100  
# #     n_chunks = len(df_merged) // chunk_size + (1 if len(df_merged) % chunk_size != 0 else 0)
# #     # processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U (original)', 'Co4U (update)']}
# #     processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U']}

# #     for i in range(n_chunks):
# #         start_idx = i * chunk_size
# #         end_idx = min((i + 1) * chunk_size, len(df_merged))
# #         processed_data['zstd'].append(np.mean(data1['zstd'][start_idx:end_idx]))
# #         processed_data['brotli'].append(np.mean(data1['brotli'][start_idx:end_idx]))
# #         processed_data['gzip'].append(np.mean(data1['gzip'][start_idx:end_idx]))
# #         #processed_data['Co4U (original)'].append(np.mean(data1['zstd_dict'][start_idx:end_idx]))
# #         processed_data['Co4U'].append(np.mean(compression_ratio[start_idx:end_idx]))

# #     return processed_data, n_chunks


# # def create_plot(file1, file2, output_file='compression_ratio.pdf'):
# #     plt.rcParams['font.family'] = 'Times New Roman'
# #     plt.rcParams['font.size'] = 21
    
# #     df1 = pd.read_csv(file1)
# #     df2 = pd.read_csv(file2)
    
# #     print("Before sorting - First few rows of first file:")
# #     print(df1.head())
# #     print("\nBefore sorting - First few rows of second file:")
# #     print(df2.head())
    
# #     processed_data, n_chunks = process_data(df1, df2)
    
# #     plt.figure(figsize=(20, 11))
# #     colors = {
# #         'zstd': '#5CA7C7', 'brotli': '#FBCE6A', 'gzip': '#383838',
# #         'Co4U': '#D4352D'
# #     }#'Co4U ':  '#9467bd''#d62728',
# #     x = np.arange(n_chunks)
    
# #     for label, color in colors.items():
# #         plt.plot(x, processed_data[label], label=label, linewidth=3, color=color)
    
# #     plt.xlabel('Message Number (10k)', fontsize=37.5, labelpad=10)
# #     plt.ylabel('Compression Ratio (%)', fontsize=37.5, labelpad=10)
# #     plt.legend(loc='center left', bbox_to_anchor=(0.79, 0.83), frameon=True,
# #               framealpha=0.9, fontsize=25.5, title='Compression Methods',
# #               title_fontsize=25.5)
# #     plt.xticks(fontsize=32)
# #     plt.yticks(np.arange(0, 100, 10), fontsize=32)
# #     plt.grid(True, linestyle='--', alpha=0.7)
# #     plt.xlim(0, n_chunks-300)
# #     plt.tight_layout()
# #     plt.savefig(output_file, format='pdf', dpi=300, bbox_inches='tight')
# #     plt.close()

# # # 使用示例
# # create_plot('multi_folder_ratio_5.csv', 'compression_results_greedy_all_5.csv')









# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import re

# def custom_sort_key(file_name):
#     """ 根据文件夹和文件名进行自定义排序 """
#     folder_order = {
#         "ct": 1, "st": 2, "creative-ups_hdr": 3, "stable-ups_hdr": 4
#     }
    
#     folder_match = re.match(r'([^/]+)/(\d+)\.log', file_name)
#     if not folder_match:
#         return (999, 999999)  # 未匹配的排到最后
    
#     folder, file_num = folder_match.groups()
#     folder_rank = folder_order.get(folder, 999)  # 未知文件夹排在最后
#     return (folder_rank, int(file_num))  # 文件按数字排序

# def filter_allowed_folders(df):
#     """只保留指定文件夹中的数据"""
#     allowed_folders = ["ct", "st", "creative-ups_hdr"]
#     # 提取文件名中的文件夹部分并检查是否在允许的文件夹列表中
#     return df[df['File'].apply(lambda x: x.split('/')[0] if '/' in x else '').isin(allowed_folders)]

# def process_data(df1, df2, chunk_size=1000):
#     """处理数据，计算每chunk_size行的平均值，并对齐文件列表"""
#     # 首先过滤数据，只保留来自指定文件夹的数据
#     df1 = filter_allowed_folders(df1)
#     df2 = filter_allowed_folders(df2)
    
#     df1 = df1.sort_values('File', key=lambda x: x.map(custom_sort_key))
#     df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

#     # 通过 merge 只保留两个数据框都包含的文件
#     df_merged = pd.merge(df1, df2[['File']], on='File', how='inner')
#     df2 = pd.merge(df2, df1[['File']], on='File', how='inner')

#     # 再次排序，确保一致
#     df_merged = df_merged.sort_values('File', key=lambda x: x.map(custom_sort_key))
#     df2 = df2.sort_values('File', key=lambda x: x.map(custom_sort_key))

#     # 处理数据
#     data1 = {
#         'zstd': pd.to_numeric(df_merged['zstd'].str.rstrip('%'), errors='coerce'),
#         'brotli': pd.to_numeric(df_merged['brotli'].str.rstrip('%'), errors='coerce'),
#         'gzip': pd.to_numeric(df_merged['gzip'].str.rstrip('%'), errors='coerce'),
#         #'zstd_dict': pd.to_numeric(df_merged['zstd_dict'].str.rstrip('%'), errors='coerce')
#     }

#     compression_ratio = df2['Compression Ratio'].values * 100  
#     n_chunks = len(df_merged) // chunk_size + (1 if len(df_merged) % chunk_size != 0 else 0)
#     # processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U (original)', 'Co4U (update)']}
#     processed_data = {key: [] for key in ['zstd', 'brotli', 'gzip', 'Co4U']}

#     for i in range(n_chunks):
#         start_idx = i * chunk_size
#         end_idx = min((i + 1) * chunk_size, len(df_merged))
#         processed_data['zstd'].append(np.mean(data1['zstd'][start_idx:end_idx]))
#         processed_data['brotli'].append(np.mean(data1['brotli'][start_idx:end_idx]))
#         processed_data['gzip'].append(np.mean(data1['gzip'][start_idx:end_idx]))
#         #processed_data['Co4U (original)'].append(np.mean(data1['zstd_dict'][start_idx:end_idx]))
#         processed_data['Co4U'].append(np.mean(compression_ratio[start_idx:end_idx]))

#     return processed_data, n_chunks


# def create_plot(file1, file2, output_file='compression_ratio_filtered.pdf'):
#     plt.rcParams['font.family'] = 'Times New Roman'
#     plt.rcParams['font.size'] = 21
    
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)
    
#     print("Before filtering and sorting - Row counts:")
#     print(f"First file: {len(df1)}")
#     print(f"Second file: {len(df2)}")
    
#     # 过滤掉数据，只保留指定文件夹的数据
#     df1_filtered = filter_allowed_folders(df1)
#     df2_filtered = filter_allowed_folders(df2)
    
#     print(f"\nAfter filtering - Row counts:")
#     print(f"First file: {len(df1_filtered)}")
#     print(f"Second file: {len(df2_filtered)}")
    
#     print("\nFirst few rows after filtering:")
#     print(df1_filtered.head())
    
#     processed_data, n_chunks = process_data(df1, df2)
    
#     plt.figure(figsize=(8, 6))
#     colors = {
#         'zstd': '#5CA7C7', 'brotli': '#FBCE6A', 'gzip': '#383838',
#         'Co4U': '#D4352D'
#     }#'Co4U ':  '#9467bd''#d62728',
#     x = np.arange(n_chunks)
    
#     for label, color in colors.items():
#         plt.plot(x, processed_data[label], label=label, linewidth=3, color=color)
    
#     plt.xlabel('Message Number (k)', fontsize=37.5, labelpad=10)
#     plt.ylabel('Compression Ratio (%)', fontsize=37.5, labelpad=10)
#     plt.legend(loc='center left', bbox_to_anchor=(0.79, 0.83), frameon=True,
#               framealpha=0.9, fontsize=25.5, title='Compression Methods',
#               title_fontsize=25.5)
#     plt.xticks(fontsize=32)
#     plt.yticks(np.arange(0, 100, 10), fontsize=32)
#     plt.grid(True, linestyle='--', alpha=0.7)
#     plt.xlim(0, 1500)
#     plt.tight_layout()
#     plt.savefig(output_file, format='pdf', dpi=600, bbox_inches='tight')
#     plt.close()

# # 使用示例
# create_plot('multi_folder_ratio_5.csv', 'compression_results_greedy_all_5.csv')


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

def custom_sort_key(file_name):
    """ 根据文件夹和文件名进行自定义排序 """
    folder_order = {
        "ct": 1, "st": 2, "creative-ups_hdr": 3, "stable-ups_hdr": 4
    }
    
    folder_match = re.match(r'([^/]+)/(\d+)\.log', file_name)
    if not folder_match:
        return (999, 999999)  # 未匹配的排到最后
    
    folder, file_num = folder_match.groups()
    folder_rank = folder_order.get(folder, 999)  # 未知文件夹排在最后
    return (folder_rank, int(file_num))  # 文件按数字排序

def filter_allowed_folders(df):
    """只保留指定文件夹中的数据"""
    allowed_folders = ["ct", "st", "creative-ups_hdr"]
    # 提取文件名中的文件夹部分并检查是否在允许的文件夹列表中
    return df[df['File'].apply(lambda x: x.split('/')[0] if '/' in x else '').isin(allowed_folders)]

def process_data(df1, df2, chunk_size=1000):
    """处理数据，计算每chunk_size行的平均值，并对齐文件列表"""
    # 首先过滤数据，只保留来自指定文件夹的数据
    df1 = filter_allowed_folders(df1)
    df2 = filter_allowed_folders(df2)
    
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

def create_plot(file1, file2, output_file='compression_ratio_filtered.pdf'):
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 8
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    df1_filtered = filter_allowed_folders(df1)
    df2_filtered = filter_allowed_folders(df2)
    
    processed_data, n_chunks = process_data(df1, df2)
    
    # 将厘米转换为英寸
    width_inches = 8 / 2.54  # 8 cm
    height_inches = 6 / 2.54 # 6 cm
    
    plt.figure(figsize=(width_inches, height_inches))
    colors = {
        'zstd': '#5CA7C7', 
        'brotli': '#FBCE6A', 
        'gzip': '#383838',
        'Co4U': '#D4352D'
    }
    
    x = np.arange(n_chunks)
    
    for label, color in colors.items():
        plt.plot(x, processed_data[label], label=label, linewidth=1.2, color=color)
    
    plt.xlabel('Message Number (k)', fontsize=9, labelpad=4)
    plt.ylabel('Compression Ratio (%)', fontsize=9, labelpad=4)
    
    # 修改图例位置
    plt.legend(
        loc='best',  
        # bbox_to_anchor=(0.9, 0.9),
        frameon=True,
        framealpha=0.9, 
        fontsize=7, 
        #title='Compression Methods',
        #title_fontsize=7
    )
    
    plt.xticks(fontsize=10)
    plt.yticks(np.arange(0, 100, 10), fontsize=10)
    
    plt.grid(True, linestyle='--', alpha=0.7, linewidth=0.5)
    plt.xlim(0, 1500)
    
    # 确保有足够的空间放置图例
    plt.tight_layout()
    
    plt.savefig(output_file, 
                format='pdf', 
                dpi=600, 
                bbox_inches='tight')
    plt.close()
# 使用示例
create_plot('multi_folder_ratio_5.csv', 'compression_results_greedy_all_5.csv')