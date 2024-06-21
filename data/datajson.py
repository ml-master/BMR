import json
import pandas as pd
import os
import openpyxl
from sklearn.model_selection import train_test_split
import cv2
from PIL import Image, ImageTk
import torchvision.transforms as transforms
to_tensor = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),]
)
# 加载 JSON 文件
def resize_image(input_image_path, output_image_path, target_size=(224, 224)):
    image = Image.open(input_image_path)
    image = image.resize(target_size, Image.ANTIALIAS)

    # 转换图片为 RGB 模式
    image = image.convert('RGB')

    # 检查输出路径是否存在，如果存在则删除
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    # 保存为 PNG 格式
    image.save(output_image_path, 'PNG')
json_file = '/home/houjiao/DataSets/GossipCop/gossipcop_v3-1_style_based_fake.json'
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化列表以存储数据
titles = []
labels = []
contents = []
type = []
image_names = []
# ##  NEWS TYPE: 0 MULTIMODAL 1 IMAGE 2 TEXT
# label 0 fake, 1 legitimate
# 处理 JSON 文件中的每个条目
for entry in data.values():
    titles.append(entry['origin_id'])
    if entry['origin_label'] == 'legitimate':
        labels.append(1)
    else:
        labels.append(0)
    contents.append(entry['generated_text'])

    # if entry['has_top_img']:
    #     type.append(0)
    # else:
    #     type.append(2)
    # 生成图片路径
    # if entry['has_top_img']:
    image_name = f"{entry['origin_id']}_top_img.png"
    image_names.append(image_name)
    image_path = '/home/houjiao/DataSets/GossipCop/top_img/' + image_name
    # ##  NEWS TYPE: 0 MULTIMODAL 1 IMAGE 2 TEXT
    if os.path.exists(image_path):
        image_open = cv2.imread(image_path)
        image_open = Image.open(image_path)
        image_tensor = to_tensor(image_open)
        image_width, image_height = image_open.size
        if len(entry['generated_text']) < 15:
            type.append(1)
        elif image_width < 224 or image_height < 224:
            resize_image(image_path, image_path)
            print("resize image ")
            type.append(0)
        else:
            type.append(0)
    else:
        type.append(2)
# 创建 DataFrame
df = pd.DataFrame({
    'image': titles,
    'label': labels,
    'content': contents,
    'type': type,
    'image_names': image_names
})
# 将 DataFrame 保存为 Excel 文件
# excel_file = '转换后的数据.xlsx'
df.to_excel('/home/houjiao/CodeFiles/work/BMR/datasets_zhunbei/gossip2/origin_do_not_modify/gossip.xlsx')
# df.to_excel(excel_file, index=False, encoding='utf-8')
print("data has save")
# -----------------------------------------------------------------
df_data = df[df['type'] == 0]
df_legitimate = df_data[df_data['label'] == 1]  # 合法新闻数据框

df_fake = df_data[df_data['label'] == 0]  # 假新闻数据框
# 分别对两个数据框进行 9:1 的划分
train_legitimate, test_legitimate = train_test_split(df_legitimate, test_size=0.1)
train_fake, test_fake = train_test_split(df_fake, test_size=0.1)


# Save the training and testing sets to separate Excel files
# 将训练集和测试集数据分别写入两个 Excel 文件中
train_file = '/home/houjiao/CodeFiles/work/BMR/datasets_zhunbei/gossip2/origin_do_not_modify/gossip_train.xlsx'
train_file2 = '/home/houjiao/CodeFiles/work/BMR/datasets_zhunbei/gossip2/origin_do_not_modify/gossip_train2.xlsx'
test_file = '/home/houjiao/CodeFiles/work/BMR/datasets_zhunbei/gossip2/origin_do_not_modify/gossip_test.xlsx'
test_file2 = '/home/houjiao/CodeFiles/work/BMR/datasets_zhunbei/gossip2/origin_do_not_modify/gossip_test2.xlsx'
# 写入训练集合法新闻数据
train_legitimate.to_excel(train_file, index=False)
# 写入训练集假新闻数据，从第二行开始写入（第一行是合法新闻数据）
train_fake.to_excel(train_file2, index=False)

# 写入测试集合法新闻数据
test_legitimate.to_excel(test_file, index=False)
# 写入测试集假新闻数据，从第二行开始写入（第一行是合法新闻数据）
test_fake.to_excel(test_file2, index=False)

