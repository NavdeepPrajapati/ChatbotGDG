from transformers import AutoTokenizer, AutoModel
import torch

class CodeBERTEmbedder:
    def __init__(self, model_name="microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    def batch_generate_embeddings(self, texts):
        inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

# Testing the embedder
if __name__ == "__main__":
    embedder = CodeBERTEmbedder()
    test_text = "Find the maximum subarray sum"
    print(embedder.generate_embedding(test_text).shape)
