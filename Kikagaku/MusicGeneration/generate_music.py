import torch
from miditok import REMI
import pretty_midi
from scipy.io.wavfile import write
import numpy as np
from .generate_model import MusicGenerator
from Kikagaku.settings import BASE_DIR
import os

def load_model():
    vocab_size = 530
    embed_dim = 256
    num_heads = 4
    num_layers = 4
    
    model = MusicGenerator(vocab_size=vocab_size, embed_dim=embed_dim, num_heads=num_heads, num_layers=num_layers)
    ckpt_path = os.path.join(BASE_DIR, 'MusicGeneration/best_MusicGenerateModel_3.ckpt')
    ckpt = torch.load(ckpt_path, map_location=torch.device("cpu"))
    state_dict = ckpt["state_dict"]
    new_state_dict = {k.replace("model.", ""): v for k, v in state_dict.items()}
    model.load_state_dict(new_state_dict)
    return model

def generate_tokens(model, max_length, start_token=128):
    model.eval()
    device = torch.device('cpu')
    input_ids = torch.tensor([[start_token]], dtype=torch.long).to(device)

    for _ in range(max_length - 1):
        with torch.no_grad():
            logits = model(input_ids)
            next_token_logits = logits[:, -1, :]
            probs = torch.softmax(next_token_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            input_ids = torch.cat([input_ids, next_token], dim=1)

    return input_ids[0].tolist()

def decode_tokens_to_midi(tokens, output_path):
    tokenizer_path = os.path.join(BASE_DIR, 'MusicGeneration/tokenizer_3.json')
    tokenizer = REMI(params=tokenizer_path)
    id_to_token = {v: k for k, v in tokenizer.vocab.items()}
    token_str_seq = [id_to_token[id] for id in tokens if id in id_to_token]
    midi= tokenizer.decode(token_str_seq)
    midi.dump_midi(output_path)

def midi_to_audio(midi_path, wav_path, rate=44100):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    audio_data = midi_data.synthesize()
    audio_int16 = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)
    write(wav_path, rate, audio_int16)