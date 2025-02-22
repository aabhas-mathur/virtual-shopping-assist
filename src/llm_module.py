from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# Define paths
BASE_MODEL_PATH = "google/gemma-2b"  # Change if you used a different base model
LORA_MODEL_PATH = "static/models/fine_tuned_gemma_2b-20250222T100555Z-001/fine_tuned_gemma_2b"

# Load the base model with quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_PATH, 
    quantization_config=quant_config,
    device_map="auto"
)

# Load LoRA adapters
model = PeftModel.from_pretrained(model, LORA_MODEL_PATH)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_PATH)

def chat(prompt):
    """Generates a response from the fine-tuned model."""
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test run
if __name__ == "__main__":
    print(chat("Find a floral skirt under $40 in size S. Is it in stock?"))
