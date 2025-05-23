import torch
from miditok import REMI
import pretty_midi
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
from .generate_model import MusicGenerator
from Kikagaku.settings import BASE_DIR
from io import BytesIO
import base64
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

def midi_to_image(midi_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = plt.cm.get_cmap('tab20', len(midi_data.instruments))
    for i, instrument in enumerate(midi_data.instruments):
        for note in instrument.notes:
            ax.plot([note.start, note.end], [note.pitch, note.pitch], linewidth=5, color=colors(i), label=instrument.name if i == 0 else "")

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('MIDI Pitch')
    ax.set_title('Colored Piano Roll by Instrument')
    ax.grid(True)

    # 凡例表示 必要ならアンコメント
    # handles = []
    # labels = []
    # for i, instrument in enumerate(midi_data.instruments):
    #     handles.append(plt.Line2D([0], [0], color=colors(i), lw=5))
    #     labels.append(instrument.name if instrument.name else f'Instrument {i+1}')

    plt.tight_layout()

    buf = BytesIO()
    format = 'jpg'
    plt.savefig(buf, format=format)
    plt.close(fig)
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64, format