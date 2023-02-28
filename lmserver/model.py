from transformers import AutoTokenizer, AutoModelForCausalLM


class LocalModel:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def generate(self, prompt, temperature=0.7, new_tokens=50):
        input_ = self.tokenizer(prompt, return_tensors='pt')
        output = self.model.generate(
            **input_,
            do_sample=True,
            temperature=temperature,
            min_new_tokens=new_tokens,
            max_new_tokens=new_tokens,
            no_repeat_ngram_size=2,
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    @classmethod
    def load(cls, name):
        tokenizer = AutoTokenizer.from_pretrained(name)
        model = AutoModelForCausalLM.from_pretrained(name)
        return cls(tokenizer, model)


def setup(name):
    if name.startswith('http'):
        raise NotImplementedError
    else:
        return LocalModel.load(name)
