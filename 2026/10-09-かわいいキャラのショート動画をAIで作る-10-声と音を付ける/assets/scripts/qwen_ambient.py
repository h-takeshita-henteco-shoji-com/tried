# 声のAI(Qwen3-TTS VoiceDesign)に、環境音を頼むとどうなるかを試す。
# 説明(instruct)に効果音の指示文、台詞(text)に擬音語を渡す。
import sys, time, torch, soundfile as sf
from qwen_tts import Qwen3TTSModel

out = sys.argv[1]
jobs = [
    ("yu", "A small, quiet outdoor hot spring pool at dusk. A thin trickle of warm water flowing in, soft continuous gurgling, an occasional tiny bubble. No wind, no music, no voices. Calm, steady, loopable.",
     "ちょろちょろ、ちょろちょろ……ぽこっ。"),
    ("door", "A wooden Japanese sliding door slowly closing inside a distant building. Soft rolling slide, then a small gentle thud at the end. Far away and muffled. No voices, no footsteps.",
     "カラカラカラ……コトン。"),
    ("light", "A single click of an old wall light switch being turned off, in a room behind a closed door. Short, small, far away and muffled. Silence after. No voices.",
     "カチッ。"),
]
m = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="mps", dtype=torch.float16)
for name, instruct, text in jobs:
    torch.manual_seed(1)
    t = time.time()
    wavs, sr = m.generate_voice_design(text=text, instruct=instruct, language="Japanese")
    f = f"{out}/{name}_qwen_1.wav"
    sf.write(f, wavs[0], sr)
    print(f, f"{len(wavs[0])/sr:.1f}s audio, {time.time()-t:.0f}s gen", flush=True)
