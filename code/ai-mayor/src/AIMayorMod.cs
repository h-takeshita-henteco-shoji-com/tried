using ICities;

namespace AIMayor
{
    // 何もしないMod。コンテンツマネージャーに表示され、有効にできることだけを確かめる。
    public class AIMayorMod : IUserMod
    {
        public string Name => "AI Mayor";

        public string Description => "AIは最高の市長になれるか(開発中)";
    }
}
