using CitiesHarmony.API;
using ICities;

namespace AIMayor
{
    // Mod の入口。有効にしたら HTTP の窓口を開き、無効にしたら閉じる。
    public class AIMayorMod : IUserMod
    {
        public string Name => "AI Mayor";

        public string Description => "AIは最高の市長になれるか(開発中)";

        public void OnEnabled()
        {
            HttpBridge.Start();
            // Harmony の準備ができたら、ダイアログの開閉に処理を差し込む。HarmonyLib は Patcher の中だけで使う
            HarmonyHelper.DoOnHarmonyReady(() => Patcher.PatchAll());
        }

        public void OnDisabled()
        {
            if (HarmonyHelper.IsHarmonyInstalled)
            {
                Patcher.UnpatchAll();
            }

            HttpBridge.Stop();
        }
    }
}
