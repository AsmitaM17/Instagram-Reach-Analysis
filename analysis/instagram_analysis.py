import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
from pathlib import Path

# Setup paths (GitHub-friendly)
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "Instagram_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

# Create outputs folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """Load data with automatic encoding detection"""
    try:
        # Try common encodings
        for encoding in ['utf-8', 'latin1', 'utf-16']:
            try:
                df = pd.read_csv(DATA_PATH, encoding=encoding)
                print(f"Successfully loaded with {encoding} encoding")
                return df
            except UnicodeDecodeError:
                continue
        raise ValueError("Failed to decode file with common encodings")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_and_visualize(df):
    """Run all analyses"""
    # 1. Reach Sources
    reach = df[['From Home', 'From Hashtags', 'From Explore', 'From Other']].sum()
    reach.plot(kind='bar', title='Reach Sources').get_figure().savefig(OUTPUT_DIR/'reach.png')
    
    # 2. Engagement
    engagement = df[['Likes', 'Comments', 'Shares', 'Saves']].mean()
    engagement.plot(kind='barh', title='Average Engagement').get_figure().savefig(OUTPUT_DIR/'engagement.png')
    
    # 3. Hashtag Word Cloud
    hashtags = ' '.join(df['Hashtags'].dropna())
    WordCloud(width=800, height=400).generate(hashtags).to_file(OUTPUT_DIR/'hashtags.png')
    
    # 4. Correlation Matrix
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.savefig(OUTPUT_DIR/'correlations.png')
    plt.close()

if __name__ == "__main__":
    print("Running Instagram Reach Analysis...")
    data = load_data()
    if data is not None:
        analyze_and_visualize(data)
        print(f"Analysis complete! Check the '{OUTPUT_DIR}' folder for results.")
