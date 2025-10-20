import re
import json
from collections import Counter
import mwparserfromhell

# Path to your downloaded Telugu Wikipedia XML dump
WIKI_XML_PATH = 'src/data/tewiki-latest-pages-articles.xml'
# Path where the Telugu word count index will be saved
OUTPUT_INDEX_PATH = 'src/te_word_counts.json'

# Regex to find all Telugu words (covers the Unicode range for Telugu script)
TELUGU_WORD_REGEX = re.compile(r'[\u0C00-\u0C7F]+')

def extract_words_from_wikitext(text):
    """Extracts and cleans Telugu words from a piece of wikitext."""
    stripped_text = mwparserfromhell.parse(text).strip_code()
    return TELUGU_WORD_REGEX.findall(stripped_text.lower())

def build_index():
    """
    Reads the Wikipedia dump, processes it, and builds a word frequency index.
    """
    print(f"Starting to process Wikipedia dump from: {WIKI_XML_PATH}")
    word_counts = Counter()
    article_count = 0

    try:
        with open(WIKI_XML_PATH, 'r', encoding='utf-8') as f:
            in_page = False
            in_text = False
            page_content = []

            for line in f:
                if '<page>' in line:
                    in_page = True
                elif '</page>' in line:
                    in_page = False
                    full_page_text = "".join(page_content)
                    words = extract_words_from_wikitext(full_page_text)
                    word_counts.update(words)
                    
                    article_count += 1
                    if article_count % 1000 == 0:
                        print(f"Processed {article_count} articles...")
                    
                    page_content = []

                elif in_page and '<text' in line:
                    in_text = True
                elif in_page and '</text>' in line:
                    in_text = False
                
                elif in_text:
                    page_content.append(line)

        print(f"\nFinished processing! Total articles: {article_count}")
        print(f"Total unique words found: {len(word_counts)}")

        print(f"Saving index to: {OUTPUT_INDEX_PATH}")
        with open(OUTPUT_INDEX_PATH, 'w', encoding='utf-8') as f:
            json.dump(word_counts, f, ensure_ascii=False, indent=4)
        
        print("Index building complete.  индех бильдинг комплете.")

    except FileNotFoundError:
        print(f"ERROR: The file was not found at {WIKI_XML_PATH}")
        print("Please make sure you have downloaded, unzipped, and placed the Wikipedia XML file in the correct directory.")

if __name__ == '__main__':
    build_index()