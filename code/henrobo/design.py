import sys, time, json, torch, soundfile as sf
from qwen_tts import Qwen3TTSModel
out, spec = sys.argv[1], json.load(open(sys.argv[2]))
m = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="mps", dtype=torch.float16)
for job in spec["jobs"]:
    for seed in spec["seeds"]:
        torch.manual_seed(seed)
        t = time.time()
        wavs, sr = m.generate_voice_design(text=spec["text"], instruct=job["instruct"], language="Japanese")
        f = f'{out}/{job["name"]}_{seed}.wav'
        sf.write(f, wavs[0], sr)
        print(f, f"{len(wavs[0])/sr:.1f}s audio, {time.time()-t:.0f}s gen", flush=True)
