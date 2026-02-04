from sentence_transformers import SentenceTransformer, util

# Load lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_match_score(resume_text: str, jd_text: str) -> int:
    # Create embeddings
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(jd_text, convert_to_tensor=True)

    # Cosine similarity (0–1)
    similarity = util.cos_sim(resume_emb, jd_emb).item()

    # Convert to percentage
    return int(similarity * 100)
