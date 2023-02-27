from transformers import AutoTokenizer, AutoModelForCausalLM


def load(name):
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name)
    return tokenizer, model


def generate(tokenizer, model, prompt, temperature=0.7, new_tokens=50):
    input = tokenizer(prompt, return_tensors='pt')
    output = model.generate(
        **input,
        do_sample=True,
        temperature=temperature,
        min_new_tokens=new_tokens,
        max_new_tokens=new_tokens,
        no_repeat_ngram_size=2,
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)
