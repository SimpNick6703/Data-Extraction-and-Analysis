import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import syllapy

nltk.download('punkt')
nltk.download('stopwords')

input_file = 'D:/OS Shared/test/20211030 Test Assignment/Input.xlsx'
output_template_file = 'D:/OS Shared/test/20211030 Test Assignment/Output.xlsx'
stopwords_folder = 'D:/OS Shared/test/20211030 Test Assignment/StopWords'
master_dict_folder = 'D:/OS Shared/test/20211030 Test Assignment/MasterDictionary'

stop_words = set()
for filename in os.listdir(stopwords_folder):
    if filename.endswith(".txt"):
        stop_words.update(read_file(os.path.join(stopwords_folder, filename)))

positive_words = set(read_file(os.path.join(master_dict_folder, 'positive-words.txt')))
negative_words = set(read_file(os.path.join(master_dict_folder, 'negative-words.txt')))

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().splitlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read().splitlines()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='cp1252') as file:
                return file.read().splitlines()
            
def extract_article(soup):
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else 'No title found'
    
    article_tag = soup.find('div', class_='td-post-content tagdiv-type')
    
    if article_tag:
        elements = article_tag.find_all(['p', 'h1', 'li'])
    else:
        elements = []
    
    article_text = '\n'.join([element.get_text(strip=True) for element in elements])
    return title, article_text

def save_article_to_file(url_id, title, article_text, output_folder='articles'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_path = os.path.join(output_folder, f'{url_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n\n{article_text}")

# df = pd.read_excel(input_file)
# for index, row in df.iterrows():
#     url_id = row['URL_ID']
#     url = row['URL']
    
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         title, article_text = extract_article(soup)
#         save_article_to_file(url_id, title, article_text)
#     else:
#         print(f"Failed to fetch the content from URL: {url}")

def fetch_and_save_article(row):
    url_id = row['URL_ID']
    url = row['URL']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title, article_text = extract_article(soup)
            save_article_to_file(url_id, title, article_text)
        else:
            print(f"Failed to fetch the content from URL: {url}")
    except Exception as e:
        print(f"Exception for URL {url}: {e}")
        
df = pd.read_excel(input_file)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_and_save_article, row) for index, row in df.iterrows()]
    for future in as_completed(futures):
        future.result()
        
def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    
    words_cleaned = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    
    positive_score = sum(1 for word in words_cleaned if word in positive_words)
    negative_score = sum(1 for word in words_cleaned if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words_cleaned) + 0.000001)
    
    avg_sentence_length = len(words_cleaned) / len(sentences)
    
    complex_words = [word for word in words_cleaned if syllapy.count(word) > 2]
    percentage_complex_words = len(complex_words) / len(words_cleaned)
    
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    avg_words_per_sentence = len(words_cleaned) / len(sentences)
    
    word_count = len(words_cleaned)
    
    syllable_count = sum(syllapy.count(word) for word in words_cleaned)
    avg_syllable_per_word = syllable_count / word_count
    
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    
    avg_word_length = sum(len(word) for word in words_cleaned) / word_count
    
    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score,
        'Avg Sentence Length': avg_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Number of Words Per Sentence': avg_words_per_sentence,
        'Complex Word Count': len(complex_words),
        'Word Count': word_count,
        'Syllable Per Word': avg_syllable_per_word,
        'Personal Pronouns': personal_pronouns,
        'Avg Word Length': avg_word_length,
    }

results_df = pd.DataFrame(results)
output_df = output_template_df.merge(results_df, on='URL_ID', how='left')

output_df.to_excel('D:/OS Shared/test/20211030 Test Assignment/Text Analysis Results.xlsx', index=False)