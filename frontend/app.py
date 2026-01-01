import streamlit as st
import requests

API_BASE = "https://book-recommender-platform.onrender.com"

st.set_page_config(page_title="Book Recommender", layout="wide")

st.title("📚 Book Recommendation Platform")
st.write("Hybrid, explainable book recommendations")

# --- Search ---
st.subheader("Search for a book")

query = st.text_input("Enter book title (e.g. python)")

books = []
if query:
    resp = requests.get(f"{API_BASE}/search", params={"q": query})
    if resp.status_code == 200:
        books = resp.json()

if books:
    book_map = {f"{b['title']} ({b['volume_id']})": b["volume_id"] for b in books}
    selected_label = st.selectbox("Select a book", list(book_map.keys()))
    selected_volume_id = book_map[selected_label]
else:
    selected_volume_id = None

# --- Recommend ---
if selected_volume_id:
    st.subheader("Recommendations")

    if st.button("Get Recommendations"):
        rec_resp = requests.get(
            f"{API_BASE}/recommend/by-book",
            params={"volume_id": selected_volume_id, "top_n": 5}
        )

        if rec_resp.status_code == 200:
            recs = rec_resp.json()

            for r in recs:
                with st.container():
                    st.markdown(f"### 📘 {r['title']}")
                    st.markdown(f"**Score:** {r['score']:.3f}")
                    st.markdown("**Why recommended:**")
                    for reason in r["reasons"]:
                        st.markdown(f"- {reason}")
                    st.divider()
        else:
            st.error("Failed to fetch recommendations")
