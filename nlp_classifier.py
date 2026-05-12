import pandas as pd
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

# 1. Load the Data
print("Loading YouTube comments...")
df = pd.read_csv("youtube_measles_comments.csv")

# 2. Setup the Zero-Shot NLP Model
# We use a multilingual model that natively understands Bengali
print("Downloading/Loading the Multilingual NLP Model (This may take a minute...)")
classifier = pipeline(
    "zero-shot-classification", 
    model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", # A fast, highly accurate multilingual model
    device=-1 # Set to 0 if you have a dedicated GPU, -1 for CPU
)

# 3. Define our Epidemiological Categories
categories = [
    "seeking medical advice or sharing symptoms",
    "vaccine hesitancy, conspiracy, or doubting the vaccine",
    "reporting hospital admission or death",
    "blaming politicians or the government",
    "religious prayer or general grief"
]

print(f"\nAnalyzing {len(df)} comments...")

# 4. Process the Comments
results = []
for index, row in df.iterrows():
    text = str(row['Comment'])
    
    # Skip empty comments
    if len(text.strip()) < 2:
        continue
        
    try:
        # The AI reads the Bengali text and assigns probabilities to our English categories
        prediction = classifier(text, categories, multi_label=False)
        
        # Get the top predicted category
        top_category = prediction['labels'][0]
        confidence = prediction['scores'][0]
        
        results.append({
            'Author': row['Author'],
            'Comment': text,
            'Category': top_category,
            'Confidence': round(confidence * 100, 2)
        })
        
        # Print progress every 20 comments
        if (index + 1) % 20 == 0:
            print(f"Processed {index + 1}/{len(df)} comments...")
            
    except Exception as e:
        print(f"Error on row {index}: {e}")

# 5. Save the Results
results_df = pd.DataFrame(results)
results_df.to_csv("nlp_categorized_comments.csv", index=False)

print("\nNLP Classification Complete!")
print("Here is the breakdown of the digital landscape:")
print(results_df['Category'].value_counts())
print("\nSaved fully categorized data to 'nlp_categorized_comments.csv'.")