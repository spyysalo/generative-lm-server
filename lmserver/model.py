import requests

from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed


class LocalModel:
    def __init__(self, tokenizer, model, name):
        self.tokenizer = tokenizer
        self.model = model
        self.name = name

    def generate(self, prompt, temperature=0.7, new_tokens=50, seed=None):
        if seed is not None:
            set_seed(seed)

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
        return cls(tokenizer, model, name)


class RemoteModel:
    def __init__(self, url):
        self.url = url
        self.name = None

    def generate(self, prompt, temperature=0.7, new_tokens=50, seed=None):
        data_in = {
            'prompt': prompt,
            'temperature': temperature,
            'min_new_tokens': new_tokens,
            'max_new_tokens': new_tokens,
            'seed': seed,
        }
        r = requests.post(self.url, json=data_in)
        data_out = r.json()
        if 'model_name' in data_out:
            self.name = data_out['model_name']
        return data_out['generation']


def setup(name):
    if name.startswith('http'):
        return RemoteModel(name)
    else:
        return LocalModel.load(name)
