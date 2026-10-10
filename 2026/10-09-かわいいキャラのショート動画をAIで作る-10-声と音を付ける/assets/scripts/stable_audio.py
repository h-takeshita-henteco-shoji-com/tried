# Stable Audio Open 1.0 で、湯の音・戸の音・灯りの音を作る。
# 使い方: python stable_audio.py <出力フォルダ> <指示文の組> <seed> [<seed> ...]
#   指示文の組: real(写実)/ real2(湯の音だけ書き直し)/ anime(アニメ向け)
import sys, time, torch, soundfile as sf
from diffusers import StableAudioPipeline, CosineDPMSolverMultistepScheduler
import diffusers.schedulers.scheduling_dpmsolver_sde as sde

# Mac(MPS)では、ノイズを足す部品(BrownianTree)に、作成時の範囲 [0.3, 500] の外の sigma が渡る。
# 最後の段では次の sigma が 0 になり、RecursionError で止まった。最初の sigma も 500.0001 で、上限をわずかに超える。
# sigma を作成時の範囲に収めてから渡す。
_orig_init = sde.BrownianTreeNoiseSampler.__init__
def _init(self, x, sigma_min, sigma_max, seed=None, transform=lambda x: x):
    _orig_init(self, x, sigma_min, sigma_max, seed, transform)
    self._lo, self._hi, self._x = float(sigma_min), float(sigma_max), x
def _call(self, sigma, sigma_next):
    clamp = lambda s: min(max(float(s), self._lo), self._hi)
    a, b = clamp(sigma), clamp(sigma_next)
    if a == b:
        return torch.randn_like(self._x)
    t0, t1 = self.transform(torch.as_tensor(a)), self.transform(torch.as_tensor(b))
    return self.tree(t0, t1) / (t1 - t0).abs().sqrt()
sde.BrownianTreeNoiseSampler.__init__ = _init
sde.BrownianTreeNoiseSampler.__call__ = _call

SETS = {
    "real": [
        ("yu", 36.0, "A small, quiet outdoor hot spring pool at dusk. A thin trickle of warm water flowing in, soft continuous gurgling, an occasional tiny bubble. No wind, no music, no voices. Calm, steady, loopable."),
        ("door", 4.0, "A wooden Japanese sliding door slowly closing inside a distant building. Soft rolling slide, then a small gentle thud at the end. Far away and muffled. No voices, no footsteps."),
        ("light", 3.0, "A single click of an old wall light switch being turned off, in a room behind a closed door. Short, small, far away and muffled. Silence after. No voices."),
    ],
    # yu は「静か」を重ねた指示文で、ほぼ無音(-62dB)になった。水の音を前に出して書き直した版。
    "real2": [
        ("yu2", 36.0, "Close-up field recording of warm water trickling and gurgling into a small stone hot spring pool. Gentle steady stream of water, soft splashing, small bubbles popping. Natural outdoor ambience at dusk. No music, no voices."),
    ],
    # 写実的すぎたため、アニメの効果音に寄せた版。大げさで、1音ずつ聞き分けやすくする。
    "anime": [
        ("yu_anime", 36.0, "Cartoon sound effect, anime style. Cute bubbling water: clear, round plip plop bubble pops, one by one, with a light trickling stream underneath. Exaggerated, playful, crisp and close. Dry, no reverb. No music, no voices."),
        ("door_anime", 3.0, "Cartoon sound effect, anime style. A Japanese wooden sliding door: a quick exaggerated swoosh slide, then one clear hollow wooden tok at the end. Punchy, crisp, easy to recognize. Dry, no reverb. No music, no voices."),
        ("light_anime", 2.0, "Cartoon sound effect, anime style. A single exaggerated light switch click, a bright crisp plastic click, then silence. Punchy and clear. Dry, no reverb. No music, no voices."),
    ],
    # yu_anime の泡の「ぽこっ」が、ぬめの「ぷに」と被った。粒のない、低く途切れない流れの音にした版。
    "yu_flow": [
        ("yu_flow_anime", 36.0, "Cartoon sound effect, anime style background. A smooth, continuous, gentle flow of warm water into a small pool: soft low steady pouring, mellow and round. No bubbles, no drips, no pops, no splashes. Simple, warm, cozy, even and constant. Dry, no reverb. No music, no voices."),
    ],
    # ぬめが動くときの音。足がないので、足音ではなく柔らかく弾む「ぷに」にする。あとで1音ずつ切り出す。
    "nume": [
        ("nume_step_anime", 4.0, "Cartoon sound effect, anime style. Tiny cute squishy steps of a small soft jelly creature: four soft, bouncy, rubbery puni puni boing pops, evenly spaced with short silence between. High pitched, adorable, gentle. Dry, no reverb. No music, no voices."),
    ],
}
negative = "Low quality, music, melody, speech, voices, singing."

out, set_name = sys.argv[1], sys.argv[2]
seeds = [int(s) for s in sys.argv[3:]] or [1]
pipe = StableAudioPipeline.from_pretrained("stabilityai/stable-audio-open-1.0", torch_dtype=torch.float32).to("mps")
# 最後の sigma が 0 だと、最後の1段で NaN になる。最小値(0.3)で止める。
pipe.scheduler = CosineDPMSolverMultistepScheduler.from_config(pipe.scheduler.config, final_sigmas_type="sigma_min")
sr = pipe.vae.sampling_rate
for name, sec, prompt in SETS[set_name]:
    for seed in seeds:
        t = time.time()
        g = torch.Generator("cpu").manual_seed(seed)
        audio = pipe(prompt, negative_prompt=negative, num_inference_steps=100,
                     audio_end_in_s=sec, num_waveforms_per_prompt=1, generator=g).audios[0]
        f = f"{out}/{name}_stableaudio_{seed}.wav"
        sf.write(f, audio.T.float().cpu().numpy(), sr)
        print(f, f"{sec:.0f}s audio, {time.time()-t:.0f}s gen", flush=True)
