#  README

## experiments

主要为实验部分相关代码以及对应图片，需统一修改，确保色调统一等

## figures

为实验部分以外的图片，整理并提交相关ppt、drawio、vsdx等源文件以及对应的Pdf图片





## 统一配置说明

颜色均使用以下颜色，后续可继续前往http://lcpmgh.com/colors/ 进行配色选取

'zstd': '#5CA7C7', 'brotli': '#FBCE6A', 'gzip': '#383838','Co4U': '#D4352D'



为确保图片的大小易于调整，我们暂时规定所有图片的宽度为17.6，高度为13.2(整页跨度)，即为



```python
plt.figure(figsize=(17.6/2.54, 13.2/2.54))


plt.savefig('figure.pdf', bbox_inches='tight')
```

字体除了图例均需保证为30（放大三倍，由于图片最后要被三分），图例可以根据大小调整，选择loc='best'

保存时的dpi = 1200



