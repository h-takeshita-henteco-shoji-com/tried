# 採用した声(B1)をクローンし、別の台詞を読ませる。Baseモデルは Mac では float32 で動かす。
import sys, json, time, torch, soundfile as sf
from qwen_tts import Qwen3TTSModel
out, spec = sys.argv[1], json.load(open(sys.argv[2]))
m = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="mps", dtype=torch.float32)
prompt = m.create_voice_clone_prompt(ref_audio=spec["ref_audio"], ref_text=spec["ref_text"])
for job in spec["jobs"]:
    for seed in spec["seeds"]:
        torch.manual_seed(seed)
        t = time.time()
        wavs, sr = m.generate_voice_clone(text=job["text"], language="Japanese", voice_clone_prompt=prompt)
        f = f'{out}/{job["name"]}_{seed}.wav'
        sf.write(f, wavs[0], sr)
        print(f.split("/")[-1], f"{len(wavs[0])/sr:.1f}s audio, {time.time()-t:.0f}s gen", flush=True)
