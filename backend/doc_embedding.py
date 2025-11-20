import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

# Load Phi-2 -- Run the first time
device = "cuda" if torch.cuda.is_available() else "cpu"

phi2 = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    trust_remote_code=True
).to(device)

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token


# Embedding function
def embed(text_list):
    all_embeddings = []

    for text in text_list:
        tokens = tokenizer(
            text,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(device)

        # Get hidden states from Phi-2
        with torch.no_grad():
            outputs = phi2(
                **tokens,
                output_hidden_states=False
            )

        # Use the LAST HIDDEN STATE
        hidden = outputs.hidden_states[-1]    # (batch, seq_len, hidden_size)

        # Mean Pooling (standard for embeddings)
        emb = hidden.mean(dim=1)              # (batch, hidden_size)

        # Move to CPU + normalize
        emb = emb.float().cpu().numpy()
        emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)

        all_embeddings.append(emb[0])

    return np.array(all_embeddings).astype("float32")



#---TESTING---#
from doc_chunking import chunks

print(f"Loaded {len(chunks)} chunks from doc_chunking.py")
emb = embed(chunks)

print(f"Embedding shape: {emb.shape}")
print(f"First embedding (first 5 values): {emb[0][:5]}")
