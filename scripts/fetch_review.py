from google_play_scraper import Sort, reviews
import pandas as pd
from tqdm import tqdm

apps = {
    "Facebook": "com.facebook.katana",
    "Instagram": "com.instagram.android",
    "Snapchat": "com.snapchat.android",
    "Twitter": "com.twitter.android"
}

total_reviews = []

for app_name, app_id in apps.items():
    print(f"Collecting reviews for → {app_name}")
    
    count = 0
    batch = 2000  # Fetch 2000 per batch
    max_reviews = 50000  # 50k per app
    
    while count < max_reviews:
        rvws, _ = reviews(
            app_id,
            lang="en",
            country="in",
            sort=Sort.NEWEST,
            count=batch,
            filter_score_with=None
        )
        if not rvws:
            break

        df = pd.DataFrame(rvws)
        df["Platform"] = app_name
        total_reviews.append(df)
        
        count += len(df)
        print(f"{count} collected...")

reviews_df = pd.concat(total_reviews, ignore_index=True)
reviews_df.to_csv("../data/raw/reviews_raw.csv", index=False)

print("Total collected:", len(reviews_df))
