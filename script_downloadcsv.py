import kagglehub
import os

# baixar o arquivo do Kaggle

os.makedirs('./arquivos', exist_ok=True)

kagglehub.dataset_download('marlesson/news-of-the-site-folhauol', path='articles.csv', output_dir='./arquivos')