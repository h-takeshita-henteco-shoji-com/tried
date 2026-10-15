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
        }

        public void OnDisabled()
        {
            HttpBridge.Stop();
        }
    }
}
