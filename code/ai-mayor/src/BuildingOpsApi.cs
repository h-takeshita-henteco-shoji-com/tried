using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 融資と、建物の画面のボタンの操作(#82)。
    // #82 の育てる期間で、AI市長は融資を受けられず、満ちた処理場を空にできず、建物を止めることもできなかった。
    // どれもゲームの画面と同じ関数を呼ぶ(EconomyPanel、CityServiceWorldInfoPanel、ZonedBuildingWorldInfoPanel)。
    public static class BuildingOpsApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/economy/loans"] = req => HttpBridge.OnMain(Loans);
            routes["/economy/loan/take"] = req => HttpBridge.OnSimulation(() => TakeLoan(req));
            routes["/economy/loan/repay"] = req => HttpBridge.OnSimulation(() => RepayLoan(req));
            routes["/building/toggle"] = req => HttpBridge.OnSimulation(() => Toggle(req));
            routes["/building/empty"] = req => HttpBridge.OnSimulation(() => Empty(req));
            routes["/building/historical"] = req => HttpBridge.OnSimulation(() => Historical(req));
            routes["/building/relocate"] = req => HttpBridge.OnSimulation(() => Relocate(req));
        }

        // ---- 融資 ----

        // 融資の枠 i は、ゲームでは1つ目・2つ目・3つ目で解禁の節目が違う(EconomyPanel.IsLoanUnlocked)
        private static bool LoanUnlocked(int i)
        {
            switch (i)
            {
                case 0: return ToolsModifierControl.IsUnlocked(UnlockManager.Feature.Loans);
                case 1: return ToolsModifierControl.IsUnlocked(UnlockManager.Feature.SecondLoan);
                case 2: return ToolsModifierControl.IsUnlocked(UnlockManager.Feature.ThirdLoan);
                default: return false;
            }
        }

        // /economy/loans  借りられる融資(銀行ごとの申し出)と、今の借入
        // 金額はゲームの画面と同じ単位。weeklyPayment は画面と同じ計算((額 + 額 × 利率) ÷ 週数)
        private static string Loans()
        {
            var eco = EconomyManager.instance;
            var sb = new StringBuilder("{\"ok\":true,\"loans\":[");
            for (int i = 0; i < EconomyManager.MAX_LOANS; i++)
            {
                sb.Append(i > 0 ? "," : "").Append("{\"index\":").Append(i).Append(",\"bank\":").Append(Json.Str(eco.GetBankName(i)))
                  .Append(",\"unlocked\":").Append(LoanUnlocked(i) ? "true" : "false");
                EconomyManager.LoanInfo[] infos;
                if (eco.GetLoanInfo(i, out infos) && infos.Length > 0)
                {
                    var o = infos[0];
                    float total = o.m_amount + o.m_amount * o.m_interest / 100f;
                    sb.Append(",\"offer\":{\"amount\":").Append(o.m_amount).Append(",\"interestPercent\":").Append(o.m_interest)
                      .Append(",\"weeks\":").Append(o.m_length)
                      .Append(",\"weeklyPayment\":").Append(Mathf.RoundToInt(total / Mathf.Max(1, o.m_length))).Append('}');
                }

                EconomyManager.Loan loan;
                if (eco.GetLoan(i, out loan))
                {
                    int weeksLeft = Mathf.CeilToInt((float)loan.m_amountLeft / Mathf.Max(1, loan.m_amountTaken) * loan.m_length);
                    sb.Append(",\"taken\":{\"amount\":").Append(loan.m_amountTaken / 100).Append(",\"left\":").Append(loan.m_amountLeft / 100)
                      .Append(",\"interestPercent\":").Append(loan.m_interestRate / 100).Append(",\"weeks\":").Append(loan.m_length)
                      .Append(",\"weeksLeft\":").Append(weeksLeft).Append('}');
                }
                else
                {
                    sb.Append(",\"taken\":null");
                }

                sb.Append('}');
            }

            return sb.Append("],\"loanExpensesPerWeek\":").Append(eco.GetLoanExpenses() / 100)
                .Append(",\"money\":").Append(eco.LastCashAmount / 100).Append('}').ToString();
        }

        // /economy/loan/take?index=0  その枠の銀行の申し出どおりに借りる(画面の「借りる」と同じ)
        private static string TakeLoan(HttpListenerRequest req)
        {
            int i = I(req, "index", -1);
            var eco = EconomyManager.instance;
            EconomyManager.Loan loan;
            EconomyManager.LoanInfo[] infos;
            if (i < 0 || i >= EconomyManager.MAX_LOANS)
            {
                return HttpBridge.Error("index must be 0, 1 or 2 (see /economy/loans)");
            }

            if (!LoanUnlocked(i))
            {
                return HttpBridge.Error("this loan is not unlocked yet");
            }

            if (eco.GetLoan(i, out loan))
            {
                return HttpBridge.Error("this loan is already taken (repay it first)");
            }

            if (!eco.GetLoanInfo(i, out infos) || infos.Length == 0)
            {
                return HttpBridge.Error("no loan offer");
            }

            var e = eco.TakeNewLoan(i, infos[0].m_amount * 100, infos[0].m_interest * 100, infos[0].m_length);
            bool ok = false;
            while (e.MoveNext())
            {
                ok = e.Current;
            }

            return ok ? "{\"ok\":true,\"index\":" + i + ",\"amount\":" + infos[0].m_amount + ",\"money\":" + eco.LastCashAmount / 100 + "}"
                : HttpBridge.Error("the game refused the loan");
        }

        // /economy/loan/repay?index=0  残りを今すぐ返す(画面の「返す」と同じ)。お金が足りなければ返せない
        private static string RepayLoan(HttpListenerRequest req)
        {
            int i = I(req, "index", -1);
            var eco = EconomyManager.instance;
            EconomyManager.Loan loan;
            if (i < 0 || i >= EconomyManager.MAX_LOANS || !eco.GetLoan(i, out loan))
            {
                return HttpBridge.Error("no loan at this index (see /economy/loans)");
            }

            var e = eco.PayLoanNow(i);
            bool ok = false;
            while (e.MoveNext())
            {
                ok = e.Current;
            }

            return ok ? "{\"ok\":true,\"index\":" + i + ",\"repaid\":" + loan.m_amountLeft / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}"
                : "{\"ok\":false,\"error\":\"not enough money to repay\",\"left\":" + loan.m_amountLeft / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}";
        }

        // ---- 建物の画面のボタン ----

        // 置かれている建物か。なければ null を返し、error に理由
        private static BuildingInfo Get(HttpListenerRequest req, out ushort id, out string error)
        {
            id = (ushort)Mathf.Clamp(I(req, "id", 0), 0, 65535);
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            if (id == 0 || id >= bs.Length || (bs[id].m_flags & Building.Flags.Created) == 0 || bs[id].Info == null)
            {
                error = HttpBridge.Error("building not found: " + id);
                return null;
            }

            error = null;
            return bs[id].Info;
        }

        // /building/toggle?id=..&active=false  サービスの建物を止める・動かす(画面の電源のボタンと同じ)。
        // 止めると働き手と維持費が0になり、サービスもしない
        private static string Toggle(HttpListenerRequest req)
        {
            ushort id;
            string error;
            var info = Get(req, out id, out error);
            if (info == null)
            {
                return error;
            }

            if (!(info.m_buildingAI is PlayerBuildingAI))
            {
                return HttpBridge.Error("only city service buildings can be turned on or off");
            }

            bool active = req.QueryString["active"] != "false";
            info.m_buildingAI.SetProductionRate(id, ref BuildingManager.instance.m_buildings.m_buffer[id], (byte)(active ? 100 : 0));
            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(info.name)
                + ",\"active\":" + (BuildingManager.instance.m_buildings.m_buffer[id].m_productionRate != 0 ? "true" : "false") + "}";
        }

        // /building/empty?id=..&active=true  埋立地・墓地を空にする(画面の「空にする」と同じ)。
        // 中身はほかの処理場・墓地(または焼却場・火葬場)へ運ばれる。空にしている間は、新しく受け入れない
        private static string Empty(HttpListenerRequest req)
        {
            ushort id;
            string error;
            var info = Get(req, out id, out error);
            if (info == null)
            {
                return error;
            }

            var ai = info.m_buildingAI;
            ref Building b = ref BuildingManager.instance.m_buildings.m_buffer[id];
            bool active = req.QueryString["active"] != "false";
            if (!ai.CanBeEmptied())
            {
                return HttpBridge.Error("this building cannot be emptied (only landfills, cemeteries and similar)");
            }

            if (active && !ai.CanBeEmptied(id, ref b))
            {
                return HttpBridge.Error("cannot empty now (the game needs another facility of the same kind with free space)");
            }

            ai.SetEmptying(id, ref b, active);
            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(info.name)
                + ",\"emptying\":" + ((b.m_flags & Building.Flags.Downgrading) != 0 ? "true" : "false") + "}";
        }

        // /building/historical?id=..&active=true  区画の建物を歴史的建造物にする(画面の印と同じ)。
        // 印の付いた建物は、レベルが上がらず、建て替わらない
        private static string Historical(HttpListenerRequest req)
        {
            ushort id;
            string error;
            var info = Get(req, out id, out error);
            if (info == null)
            {
                return error;
            }

            var ai = info.m_buildingAI;
            ref Building b = ref BuildingManager.instance.m_buildings.m_buffer[id];
            bool canSet;
            ai.IsHistorical(id, ref b, out canSet);
            if (!canSet)
            {
                return HttpBridge.Error("this building cannot be marked historical");
            }

            bool active = req.QueryString["active"] != "false";
            ai.SetHistorical(id, ref b, active);
            bool now = ai.IsHistorical(id, ref b, out canSet);
            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(info.name) + ",\"historical\":" + (now ? "true" : "false") + "}";
        }

        // ---- 建物を移す ----

        // /building/relocate?id=..&x=..&z=..&angle=0(または facing=north)&pay=true  建物を別の場所へ移す(#82)。
        // ゲームの建物の画面の「移す」と同じ処理(BuildingTool の CreateBuilding が呼ぶ BuildingManager.RelocateBuilding)。
        // 費用は建設費の1/5(BuildingAI.GetRelocationCost)。置ける場所かは BuildingTool.CheckSpace と CheckBuildPosition で調べる
        private static string Relocate(HttpListenerRequest req)
        {
            ushort id;
            string error;
            var info = Get(req, out id, out error);
            if (info == null)
            {
                return error;
            }

            var bs = BuildingManager.instance.m_buildings.m_buffer;
            if (bs[id].m_parentBuilding != 0 || !(info.m_buildingAI is PlayerBuildingAI) || MapApi.IsNetPart(ref bs[id]))
            {
                return HttpBridge.Error("only service buildings can be relocated (not zoned buildings, sub buildings, or net parts)");
            }

            var pos = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float angleDeg = F(req, "angle", 0f);
            string facing = req.QueryString["facing"];
            if (!string.IsNullOrEmpty(facing))
            {
                angleDeg = CityApi.FacingToAngle(facing);
                if (float.IsNaN(angleDeg))
                {
                    return HttpBridge.Error("bad facing: " + facing + " (north / northeast / east / ... / northwest, or degrees clockwise from north)");
                }
            }

            float angle = angleDeg * Mathf.Deg2Rad;
            bool pay = req.QueryString["pay"] != "false";
            // test=true なら、移せるかを確かめて、移さずに返す(#125。局と市長が、移す前に試す)。壊したものとする相手も渡せる
            bool test = req.QueryString["test"] == "true";
            var assumed = test ? Assumed.Parse(req) : null;
            int cost = info.m_buildingAI.GetRelocationCost();
            var eco = EconomyManager.instance;
            if (pay && !test && eco.PeekResource(EconomyManager.Resource.Construction, cost) != cost)
            {
                return "{\"ok\":false,\"error\":\"not enough money\",\"cost\":" + cost / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}";
            }

            // 壊した・差し替えたものとする区間は、判定のあいだだけ街に反映する(#125)
            float minY, maxY, buildingY;
            ulong[] segBuf, bldBuf;
            var undo = assumed != null && assumed.HasVirtual ? assumed.Begin() : null;
            try
            {
                // 置ける場所か。ゲームの道具と同じく、建物の型が位置を直すことがある(岸に置く建物など)
                Building.SampleBuildingHeight(pos, angle, info.m_cellWidth, info.m_cellLength, info, out minY, out maxY, out buildingY);
                pos.y = buildingY;
                var seg = default(ColossalFramework.Math.Segment3);
                int productionRate, constructionCost;
                var posErrors = info.m_buildingAI.CheckBuildPosition(id, ref pos, ref angle, 0f, 0f, ref seg, out productionRate, out constructionCost);
                segBuf = new ulong[(NetManager.instance.m_segments.m_buffer.Length + 63) >> 6];
                bldBuf = new ulong[(bs.Length + 63) >> 6];
                var spaceErrors = BuildingTool.CheckSpace(info, info.m_placementMode, id, pos, minY, buildingY + info.m_collisionHeight, angle,
                    info.m_cellWidth, info.m_cellLength, true, segBuf, bldBuf);
                string coll = null;
                if (test)
                {
                    bool blocking;
                    coll = UpgradeApi.CollidingJson(segBuf, bldBuf, assumed, out blocking);
                    // 断る相手がすべて「壊したもの」なら、ぶつからないとみなす(place_building の試しと同じ)
                    if (assumed.Any && !blocking)
                    {
                        spaceErrors &= ~ToolBase.ToolErrors.ObjectCollision;
                    }
                }

                var errors = posErrors | spaceErrors;
                if (errors != ToolBase.ToolErrors.None)
                {
                    // ぶつかった相手を返す(#82)。ゲームの判定(CheckSpaceImpl)は、移す建物そのものと、その建物の道や管
                    // (IgnoreRelocateSegments)を除いている。それでも断られるなら、相手は別の道路や建物。
                    // 相手が空で断られるときのため、建物の型の判定(CheckBuildPosition)と場所の判定(CheckSpace)の理由を分けて返す(#107)。
                    // 区画に建つ建物とぶつかるときは、試しの判定(test=true)では断り、ゲームの道具は取り壊して置く
                    return "{\"ok\":false,\"error\":\"cannot relocate here\",\"reasons\":" + Json.Str(errors.ToString())
                        + ",\"positionReasons\":" + Json.Str(posErrors.ToString()) + ",\"spaceReasons\":" + Json.Str(spaceErrors.ToString())
                        + ",\"collidingBuildings\":" + Bits(bldBuf, 20) + ",\"collidingSegments\":" + Bits(segBuf, 20)
                        + (coll != null ? ",\"colliding\":" + coll : "") + "}";
                }

                if (test)
                {
                    return "{\"ok\":true,\"test\":true,\"moved\":false,\"id\":" + id + ",\"prefab\":" + Json.Str(info.name)
                        + ",\"x\":" + Mathf.RoundToInt(pos.x) + ",\"z\":" + Mathf.RoundToInt(pos.z)
                        + ",\"angleUsed\":" + Mathf.RoundToInt(angle * Mathf.Rad2Deg)
                        + ",\"cost\":" + cost / 100 + ",\"enoughMoney\":" + (eco.LastCashAmount >= cost ? "true" : "false") + "}";
                }
            }
            finally
            {
                if (undo != null)
                {
                    Assumed.Restore(undo);
                }
            }

            // 本番: 区画に建つ建物とぶつかるなら、ゲームの道具と同じく取り壊す(test=false)
            Array.Clear(segBuf, 0, segBuf.Length);
            Array.Clear(bldBuf, 0, bldBuf.Length);
            BuildingTool.CheckSpace(info, info.m_placementMode, id, pos, minY, buildingY + info.m_collisionHeight, angle,
                info.m_cellWidth, info.m_cellLength, false, segBuf, bldBuf);
            if (pay)
            {
                eco.FetchResource(EconomyManager.Resource.Construction, cost, info.m_class);
            }

            BuildingManager.instance.RelocateBuilding(id, pos, angle);
            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(info.name)
                + ",\"x\":" + Mathf.RoundToInt(pos.x) + ",\"z\":" + Mathf.RoundToInt(pos.z)
                + ",\"angleUsed\":" + Mathf.RoundToInt(angle * Mathf.Rad2Deg)
                + ",\"cost\":" + cost / 100 + ",\"paid\":" + (pay ? "true" : "false") + "}";
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }

        private static int I(HttpListenerRequest req, string key, int fallback)
        {
            int v;
            string s = req.QueryString[key];
            return s != null && int.TryParse(s, NumberStyles.Integer, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }

        // ビットの並びから、立っている番号を最大 limit 件、JSON の配列で返す
        private static string Bits(ulong[] buf, int limit)
        {
            var sb = new StringBuilder("[");
            int n = 0;
            for (int i = 0; i < buf.Length && n < limit; i++)
            {
                ulong w = buf[i];
                for (int b = 0; w != 0 && b < 64 && n < limit; b++)
                {
                    if ((w & (1UL << b)) != 0)
                    {
                        sb.Append(n > 0 ? "," : "").Append(i * 64 + b);
                        n++;
                        w &= ~(1UL << b);
                    }
                }
            }

            return sb.Append(']').ToString();
        }
    }
}
