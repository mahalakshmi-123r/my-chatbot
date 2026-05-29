from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve(query_embedding,
             document_embeddings):

    similarities = cosine_similarity(
        [query_embedding],
        document_embeddings
    )

    best_match = np.argmax(similarities)

    return best_match
