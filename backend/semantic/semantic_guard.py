from sentence_transformers import SentenceTransformer, util

class SemanticGuard:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # High-risk intent examples
        self.policy_violation_examples = [
            "how to bypass regulations",
            "avoid compliance requirements",
            "evade government rules",
            "exploit legal loopholes",
            "hide financial information"
        ]

        self.speculative_examples = [
            "this might apply",
            "it could be possible",
            "likely applies",
            "probably impacts companies"
        ]

        # Precompute embeddings
        self.policy_embeddings = self.model.encode(
            self.policy_violation_examples,
            convert_to_tensor=True
        )
        self.speculative_embeddings = self.model.encode(
            self.speculative_examples,
            convert_to_tensor=True
        )

    def check_policy_violation(self, text: str) -> bool:
        text_emb = self.model.encode(text, convert_to_tensor=True)
        score = util.cos_sim(text_emb, self.policy_embeddings).max()
        return score > 0.65

    def check_speculation(self, text: str) -> bool:
        text_emb = self.model.encode(text, convert_to_tensor=True)
        score = util.cos_sim(text_emb, self.speculative_embeddings).max()
        return score > 0.60
