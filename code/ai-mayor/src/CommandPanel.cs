using ColossalFramework.UI;
using ICities;
using UnityEngine;

namespace AIMayor
{
    // AI市長が呼んだ道具、判断の理由、ゲームのダイアログを、ゲーム画面の左上に流すパネル。新しい行が上。
    // プレイヤーの操作は止めない(モーダルにしない)。× で閉じても、次の道具が始まると開き直す。
    // ゲームの既定のフォントでは日本語が出ない恐れがあるので、見出しは英数字にしている(未確認)。
    public class CommandPanel : UIPanel
    {
        private const int Lines = 14;
        private const float W = 720f;
        private const float H = 420f;

        private static CommandPanel instance;
        private UILabel body;
        private int shown = -1;

        public static void Create()
        {
            if (instance != null)
            {
                return;
            }

            instance = (CommandPanel)UIView.GetAView().AddUIComponent(typeof(CommandPanel));
        }

        public static void DestroyPanel()
        {
            if (instance != null)
            {
                Object.Destroy(instance.gameObject);
                instance = null;
            }
        }

        // メインスレッドから毎フレーム呼ぶ。記録が変わったときだけ描き直す
        public static void Tick()
        {
            if (instance == null || instance.body == null)
            {
                return;
            }

            int v = CommandLog.Version;
            if (v == instance.shown)
            {
                return;
            }

            instance.shown = v;
            instance.body.text = CommandLog.Render(Lines);
            if (CommandLog.TakeNewStart() && !instance.isVisible)
            {
                instance.Show();
            }
        }

        public override void Start()
        {
            base.Start();
            name = "AIMayorCommandPanel";
            backgroundSprite = "MenuPanel2";
            size = new Vector2(W, H);
            // 右寄せは画面の縦横比によってはみ出すので、左上に置く(ドラッグで動かせる)
            relativePosition = new Vector3(20f, 80f);

            var drag = AddUIComponent<UIDragHandle>();
            drag.target = this;
            drag.size = new Vector2(W, 40f);
            drag.relativePosition = Vector3.zero;

            var title = AddUIComponent<UILabel>();
            title.text = "AI Mayor - MCP commands / reasons";
            title.relativePosition = new Vector3(14f, 12f);

            var close = AddUIComponent<UIButton>();
            close.normalBgSprite = "buttonclose";
            close.hoveredBgSprite = "buttonclosehover";
            close.pressedBgSprite = "buttonclosepressed";
            close.size = new Vector2(32f, 32f);
            close.relativePosition = new Vector3(W - 38f, 4f);
            close.eventClick += (c, p) => Hide();

            body = AddUIComponent<UILabel>();
            body.autoSize = false;
            body.wordWrap = true; // 理由の行は長いので折り返す。はみ出した古い行は下で切れる
            body.processMarkup = true;
            body.textScale = 0.75f;
            body.size = new Vector2(W - 28f, H - 56f);
            body.relativePosition = new Vector3(14f, 46f);
            body.text = "waiting for commands...";
        }
    }

    // 街を開いたらパネルを作り、閉じたら片付ける
    public class CommandPanelLoader : LoadingExtensionBase
    {
        public override void OnLevelLoaded(LoadMode mode)
        {
            // マップエディター(NewMap、LoadMap)でも作る。エディター用の道具の記録も残すため
            if (mode == LoadMode.NewGame || mode == LoadMode.LoadGame || mode == LoadMode.NewGameFromScenario
                || mode == LoadMode.NewMap || mode == LoadMode.LoadMap)
            {
                var meta = SimulationManager.instance.m_metaData;
                CommandLog.StartLogFile(meta != null ? meta.m_CityName : "?");
                CommandPanel.Create();
                DialogWatcher.Create();
            }
        }

        public override void OnLevelUnloading()
        {
            DialogWatcher.DestroyWatcher();
            CommandPanel.DestroyPanel();
        }
    }
}
