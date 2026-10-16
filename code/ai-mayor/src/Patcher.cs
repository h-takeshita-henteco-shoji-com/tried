using System;
using System.Reflection;
using ColossalFramework.UI;
using HarmonyLib;
using UnityEngine;

namespace AIMayor
{
    // Harmony でゲームの関数の後ろに処理を差し込む。HarmonyLib を使うのはこのクラスだけにする。
    // IUserMod から直接 HarmonyLib を参照すると、Harmony の MOD がないときに Mod ごと読めなくなるため。
    //
    // 差し込む先:
    // - UIView.PushModal: ダイアログ(画面を止める窓)が開いた
    // - UIView.PopModal / PopAllModal: ダイアログが閉じた
    public static class Patcher
    {
        private const string Id = "com.henteco.aimayor";
        private static bool patched;

        public static void PatchAll()
        {
            if (patched)
            {
                return;
            }

            var harmony = new Harmony(Id);
            var push = new HarmonyMethod(typeof(Patcher).GetMethod("PushPostfix", BindingFlags.Static | BindingFlags.NonPublic));
            var pop = new HarmonyMethod(typeof(Patcher).GetMethod("PopPostfix", BindingFlags.Static | BindingFlags.NonPublic));
            int count = 0;
            const BindingFlags all = BindingFlags.Static | BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly;
            foreach (var m in typeof(UIView).GetMethods(all))
            {
                if (m.Name == "PushModal")
                {
                    harmony.Patch(m, postfix: push);
                    count++;
                }
                else if (m.Name == "PopModal" || m.Name == "PopAllModal")
                {
                    harmony.Patch(m, postfix: pop);
                    count++;
                }
            }

            patched = true;
            DialogWatch.HooksActive = count > 0;
            Debug.Log("[AIMayor] Harmony patched " + count + " UIView methods");
        }

        public static void UnpatchAll()
        {
            if (!patched)
            {
                return;
            }

            new Harmony(Id).UnpatchAll(Id);
            patched = false;
            DialogWatch.HooksActive = false;
            Debug.Log("[AIMayor] Harmony unpatched");
        }

        // 引数の名前が版によって違っても動くよう、__args で受け取る。最初の引数が開いた画面
        private static void PushPostfix(object[] __args)
        {
            try
            {
                if (__args != null && __args.Length > 0)
                {
                    DialogWatch.OnPushed(__args[0] as UIComponent);
                }
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] PushPostfix: " + e.Message);
            }
        }

        private static void PopPostfix()
        {
            try
            {
                DialogWatch.OnPopped();
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] PopPostfix: " + e.Message);
            }
        }
    }
}
