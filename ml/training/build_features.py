from app.features.text.tfidf import load_books, build_tfidf
from app.features.metadata.category_features import build_category_features
from app.features.metadata.popularity import build_popularity
from app.features.skill_level.classifier import classify_skill_level

def run():
    books = load_books()
    build_tfidf(books)
    build_category_features()
    popularity = build_popularity()
    skill = classify_skill_level()

    print("Feature engineering completed.")
    print("Books:", len(books))
    print("Popularity rows:", len(popularity))
    print("Skill labels:", skill["skill_level"].value_counts())

if __name__ == "__main__":
    run()
