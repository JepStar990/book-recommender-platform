# 📚Hybrid Book Recommendation Platform

A production-grade, explainable book recommendation system leveraging public metadata from the Google Books ecosystem. This platform delivers relevant and transparent recommendations without relying on user ratings or interaction history, effectively solving the cold-start problem.

🌐 **Live Deployment**

- **Frontend (Streamlit):** [Book Recommender Platform](https://book-recommender-platform-p5pgpsezpns5urmkbqgqv6.streamlit.app/)
- **Backend API (FastAPI on Render):** [FastAPI Backend](https://book-recommender-platform.onrender.com)

🚀 **Project Motivation**

Traditional book discovery platforms often face significant challenges:

- Cold-start problem: Heavy dependence on user interaction data
- Popularity bias: Over-recommendation of bestsellers
- Lack of transparency: Unexplained "black-box" recommendations

This project demonstrates a senior-grade recommender system that:

- Operates without user feedback or historical data
- Handles cold-start scenarios gracefully
- Provides fully explainable recommendations
- Deploys entirely on free-tier infrastructure

🧠 **Core Features**

🔄 **Hybrid Recommendation Engine**

- Content-based similarity using TF-IDF
- Category overlap analysis
- Popularity-aware weighting
- Skill-level progression modeling (beginner → advanced)

📖 **Explainable AI**

- Human-readable justification for every recommendation
- Transparent, deterministic logic (no black-box models)
- Audit-ready decision trails

🏗️ **Production-Ready Architecture**

- FastAPI backend with comprehensive validation
- Rate limiting and CORS configuration
- Health checks and startup optimization
- Streamlit frontend with real-time interaction

💸 **Cost-Efficient Deployment**

- Backend: Render (free tier)
- Frontend: Streamlit Community Cloud
- Database: DuckDB (file-based, zero-cost)

🏗️ **System Architecture**

```
User Browser
     ↓
Streamlit Frontend (UI)
     ↓  HTTPS
FastAPI Backend (Render)
     ↓
Hybrid Recommender Engine
     ↓
DuckDB (Book Metadata & Features)
```

### Component Responsibilities

| Component       | Responsibility                                    |
|------------------|--------------------------------------------------|
| Streamlit UI     | User search, selection, and result display       |
| FastAPI API      | Request validation, orchestration, and response formatting |
| Recommender Engine| Hybrid scoring and ranking logic                  |
| Explainability Layer| Generation of human-readable justifications     |
| DuckDB           | Lightweight analytics and metadata storage        |
| GitHub Actions    | Continuous integration and deployment pipelines   |

🔁 **Recommendation Workflow**

1. **User Input:** User searches for a book via the frontend interface
2. **Initial Search:** Frontend calls `/search` endpoint
3. **Selection:** User selects a target book from search results
4. **Recommendation Request:** Frontend calls `/recommend/by-book` endpoint
5. **Backend Processing:**
   - Computes hybrid similarity scores
   - Generates explanatory justifications
   - Ranks results by relevance
6. **Response:** JSON payload returned to frontend
7. **Display:** Frontend renders ranked recommendations with explanations

🧪 **Recommendation Methodology**

### Hybrid Scoring Formula

```
Final Score = 
  0.45 × Content Similarity (TF-IDF)
+ 0.25 × Category Overlap
+ 0.20 × Popularity Score
+ 0.10 × Skill-Level Match
```

### Strategic Advantages

- Cold-start resilience: Functions without user history
- Balanced recommendations: Avoids single-metric bias
- Transparent tuning: Weight adjustments directly impact explainability

📊 **Offline Evaluation Framework**

Without access to user interaction data, the system employs industry-standard proxy metrics:

| Metric                        | Purpose                                 |
|-------------------------------|-----------------------------------------|
| Precision@K (category-based)  | Relevance approximation                 |
| Intra-list diversity          | Redundancy prevention                   |
| Novelty scoring               | Popularity bias mitigation              |
| Catalog coverage              | Recommendation breadth assessment        |

This evaluation approach aligns with academic standards for cold-start recommender systems.

🛡️ **Production Considerations**

- Input validation with Pydantic models
- Global exception handling and structured logging
- Rate limiting to prevent API abuse
- CORS configuration for secure frontend-backend communication
- Startup optimization with model preloading
- Timeout and retry logic for reliable frontend-backend communication

💰 **Cost Structure**

| Component            | Monthly Cost |
|----------------------|--------------|
| Render Backend        | $0          |
| Streamlit Frontend    | $0          |
| DuckDB Storage        | $0          |
| GitHub Actions        | $0          |
| Google Books API      | $0          |
| **Total**            | **$0**      |

⚠️ **Current Limitations**

The system makes explicit design trade-offs:

- No user personalization or collaborative filtering
- Metadata-only recommendations (no content analysis)
- Free-tier cold starts on Render
- Limited to Google Books metadata availability

These limitations represent conscious architectural decisions rather than oversights.

🔮 **Roadmap & Future Enhancements**

- User profile creation and implicit feedback integration
- Embedding-based semantic similarity (Sentence Transformers)
- Redis caching for performance optimization
- Authentication and personalized recommendation history
- PostgreSQL/vector database migration
- Online A/B testing framework for continuous evaluation

🧑‍💻 **Technology Stack**

- Backend: FastAPI, Gunicorn
- Frontend: Streamlit
- Machine Learning: scikit-learn, NumPy
- Database: DuckDB
- CI/CD: GitHub Actions
- Hosting: Render, Streamlit Cloud

📌 **Demonstrative Value**

This project showcases:

- End-to-end ML system design and implementation
- Production-grade API development best practices
- Recommender systems engineering under constraints
- Explainable AI principles in practice
- Cost-optimized cloud architecture
- Senior-level technical decision-making

📄 **License**

MIT License

