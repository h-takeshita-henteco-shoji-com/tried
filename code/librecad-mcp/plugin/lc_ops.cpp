// 命令の中身。LibreCAD 本体の内部の部品(RS_Document など)を直接使う。
// 本体の実行ファイルは C++ の記号を公開しているので、link 時は -undefined dynamic_lookup で済ませる。
// 本体のソース(v2.2.1)の header が要る。build の手順は ../README.md
#include "lc_ops.h"

#include <QApplication>
#include <QBuffer>
#include <QDateTime>
#include <QDir>
#include <QFileInfo>
#include <QJsonArray>
#include <QMainWindow>
#include <QMdiArea>
#include <QMdiSubWindow>
#include <QPixmap>
#include <QStandardPaths>

#include <memory>

#include "rs.h"
#include "rs_arc.h"
#include "rs_block.h"
#include "rs_blocklist.h"
#include "rs_circle.h"
#include "rs_dimaligned.h"
#include "rs_dimension.h"
#include "rs_dimlinear.h"
#include "rs_document.h"
#include "rs_ellipse.h"
#include "rs_graphic.h"
#include "rs_graphicview.h"
#include "rs_hatch.h"
#include "rs_insert.h"
#include "rs_layer.h"
#include "rs_layerlist.h"
#include "rs_line.h"
#include "rs_math.h"
#include "rs_modification.h"
#include "rs_mtext.h"
#include "rs_pen.h"
#include "rs_point.h"
#include "rs_polyline.h"
#include "rs_text.h"
#include "lc_undosection.h"

// 本体の画面(QC_ApplicationWindow)のうち、使う関数だけを宣言する。
// 名前と引数が同じなら、本体の関数にそのままつながる。重い header を読まずに済ませるため。
class QC_ApplicationWindow {
public:
    // 本体では unique_ptr の参照を返す。戻り値の型は記号名に入らないが、受け方は合わせる必要がある
    static std::unique_ptr<QC_ApplicationWindow> &getAppWindow();
    RS_Document *getDocument() const;
    RS_GraphicView *getGraphicView() const;
    void slotFileOpen(const QString &fileName);
    void slotFileNewNew();
};

// 図面の窓(QC_MDIWindow)。最初の基底が QMdiSubWindow なので、同じ番地のまま使える
class QC_MDIWindow {
public:
    RS_Document *getDocument() const;
};

namespace {

QC_ApplicationWindow *appWin() { return QC_ApplicationWindow::getAppWindow().get(); }

QJsonArray g_log;  // AI から受けた命令の記録

QJsonObject fail(const QString &msg)
{
    QJsonObject o;
    o["ok"] = false;
    o["error"] = msg;
    return o;
}

QJsonObject okObj()
{
    QJsonObject o;
    o["ok"] = true;
    return o;
}

// AI が open / save_as した図面のパス。#136 で、起動時に開く名前のない空の図面が前に出て、
// AI の命令がそちらに効き、図面が空になったように見えた。命令の前に、この図面の窓を前に戻す
QString g_docPath;

void keepDocActive()
{
    auto *app = appWin();
    if (!app || g_docPath.isEmpty()) return;
    auto *area = reinterpret_cast<QMainWindow *>(app)->findChild<QMdiArea *>();
    if (!area) return;
    for (QMdiSubWindow *sub : area->subWindowList()) {
        if (QString(sub->metaObject()->className()) != "QC_MDIWindow") continue;
        RS_Document *d = reinterpret_cast<QC_MDIWindow *>(sub)->getDocument();
        if (d && QFileInfo(d->getFilename()).absoluteFilePath() == g_docPath) {
            if (area->activeSubWindow() != sub) {
                area->setActiveSubWindow(sub);
                QApplication::processEvents();
            }
            return;
        }
    }
}

RS_Document *curDoc()
{
    auto *app = appWin();
    if (!app) return nullptr;
    keepDocActive();
    return app->getDocument();
}

RS_GraphicView *curView()
{
    auto *app = appWin();
    if (!app) return nullptr;
    keepDocActive();
    return app->getGraphicView();
}

// 開いている図面を映している部品(QG_GraphicView)を探す。画面の画像を撮るため。
QWidget *curViewWidget()
{
    auto *app = appWin();
    if (!app) return nullptr;
    keepDocActive();
    auto *mw = reinterpret_cast<QMainWindow *>(app);
    auto *area = mw->findChild<QMdiArea *>();
    QMdiSubWindow *sub = area ? area->activeSubWindow() : nullptr;
    if (!sub && area && !area->subWindowList().isEmpty()) sub = area->subWindowList().last();
    if (!sub) return nullptr;
    for (QWidget *w : sub->findChildren<QWidget *>())
        if (QString(w->metaObject()->className()) == "QG_GraphicView") return w;
    return nullptr;
}

void refresh(RS_Document *doc)
{
    doc->calculateBorders();
    if (auto *v = curView()) v->redraw();
}

QJsonArray pt(const RS_Vector &v) { return QJsonArray{v.x, v.y}; }

RS_Vector vec(const QJsonValue &v)
{
    QJsonArray a = v.toArray();
    return RS_Vector(a.at(0).toDouble(), a.at(1).toDouble());
}

double deg(double rad) { return rad * 180.0 / M_PI; }
double rad(double d) { return d * M_PI / 180.0; }

QString typeName(RS2::EntityType t)
{
    switch (t) {
    case RS2::EntityPoint: return "point";
    case RS2::EntityLine: return "line";
    case RS2::EntityPolyline: return "polyline";
    case RS2::EntityArc: return "arc";
    case RS2::EntityCircle: return "circle";
    case RS2::EntityEllipse: return "ellipse";
    case RS2::EntitySolid: return "solid";
    case RS2::EntityMText: return "mtext";
    case RS2::EntityText: return "text";
    case RS2::EntityInsert: return "insert";
    case RS2::EntityHatch: return "hatch";
    case RS2::EntityDimAligned: return "dim_aligned";
    case RS2::EntityDimLinear: return "dim_linear";
    case RS2::EntityDimRadial: return "dim_radial";
    case RS2::EntityDimDiametric: return "dim_diametric";
    case RS2::EntityDimAngular: return "dim_angular";
    case RS2::EntityDimLeader: return "dim_leader";
    case RS2::EntitySpline: return "spline";
    case RS2::EntitySplinePoints: return "spline_points";
    case RS2::EntityImage: return "image";
    case RS2::EntityConstructionLine: return "construction_line";
    default: return QString("type_%1").arg(int(t));
    }
}

bool isDim(RS2::EntityType t)
{
    return t == RS2::EntityDimAligned || t == RS2::EntityDimLinear || t == RS2::EntityDimRadial ||
           t == RS2::EntityDimDiametric || t == RS2::EntityDimAngular;
}

QJsonObject entityJson(RS_Entity *e, bool deep);

QJsonArray childrenJson(RS_EntityContainer *c, bool deep)
{
    QJsonArray arr;
    for (RS_Entity *ch : *c)
        if (ch && !ch->isUndone()) arr.append(entityJson(ch, deep));
    return arr;
}

// 図形の中身を JSON にする。どの図形にも、外形(bbox)と画層と色を付ける。
QJsonObject entityJson(RS_Entity *e, bool deep)
{
    QJsonObject o;
    const RS2::EntityType t = e->rtti();
    o["id"] = QString::number(e->getId());
    o["type"] = typeName(t);
    RS_Layer *l = e->getLayer(true);
    o["layer"] = l ? l->getName() : "";
    RS_Pen pen = e->getPen(true);
    o["color"] = pen.getColor().name();
    o["linetype"] = int(pen.getLineType());
    o["bbox"] = QJsonArray{pt(e->getMin()), pt(e->getMax())};

    switch (t) {
    case RS2::EntityPoint:
        o["p"] = pt(static_cast<RS_Point *>(e)->getPos());
        break;
    case RS2::EntityLine: {
        auto *x = static_cast<RS_Line *>(e);
        o["p1"] = pt(x->getStartpoint());
        o["p2"] = pt(x->getEndpoint());
        o["length"] = x->getLength();
        break;
    }
    case RS2::EntityArc: {
        auto *x = static_cast<RS_Arc *>(e);
        o["center"] = pt(x->getCenter());
        o["r"] = x->getRadius();
        o["a1"] = deg(x->getAngle1());
        o["a2"] = deg(x->getAngle2());
        o["reversed"] = x->isReversed();
        o["p1"] = pt(x->getStartpoint());
        o["p2"] = pt(x->getEndpoint());
        break;
    }
    case RS2::EntityCircle: {
        auto *x = static_cast<RS_Circle *>(e);
        o["center"] = pt(x->getCenter());
        o["r"] = x->getRadius();
        break;
    }
    case RS2::EntityText: {
        auto *x = static_cast<RS_Text *>(e);
        o["text"] = x->getText();
        o["p"] = pt(x->getInsertionPoint());
        o["height"] = x->getHeight();
        o["font"] = x->getStyle();
        o["angle"] = deg(x->getAngle());
        break;
    }
    case RS2::EntityMText: {
        auto *x = static_cast<RS_MText *>(e);
        o["text"] = x->getText();
        o["p"] = pt(x->getInsertionPoint());
        o["height"] = x->getHeight();
        o["font"] = x->getStyle();
        o["angle"] = deg(x->getAngle());
        break;
    }
    case RS2::EntityPolyline: {
        auto *x = static_cast<RS_Polyline *>(e);
        QJsonArray pts;
        bool first = true;
        for (RS_Entity *s : *x) {
            if (!s || s->isUndone()) continue;
            if (first) { pts.append(pt(s->getStartpoint())); first = false; }
            pts.append(pt(s->getEndpoint()));
        }
        // 閉じる線分があれば、最後の点は最初の点と同じなので落とす
        if (x->isClosed() && pts.size() > 1 && pts.first() == pts.last()) pts.removeLast();
        o["points"] = pts;
        o["closed"] = x->isClosed();
        break;
    }
    case RS2::EntityInsert: {
        auto *x = static_cast<RS_Insert *>(e);
        o["block"] = x->getName();
        o["p"] = pt(x->getInsertionPoint());
        o["scale"] = pt(x->getScale());
        o["angle"] = deg(x->getAngle());
        if (deep) o["children"] = childrenJson(x, false);
        break;
    }
    case RS2::EntityHatch: {
        auto *x = static_cast<RS_Hatch *>(e);
        o["solid"] = x->isSolid();
        o["pattern"] = x->getPattern();
        o["area"] = x->getTotalArea();
        break;
    }
    default:
        break;
    }
    if (isDim(t)) {
        auto *x = static_cast<RS_Dimension *>(e);
        // label は図面に書かれた文字。空か "<>" なら、測った値をそのまま出す。
        // measured は、線の長さから LibreCAD が計算した表示用の値($DIMLFAC などをかけた後)。
        // distance は、倍率をかける前の線の長さ。label と食い違えば、文字だけ古い寸法。
        o["label"] = x->getLabel(false);
        o["shown"] = x->getLabel(true);
        o["measured"] = x->getMeasuredLabel();
        o["defpoint"] = pt(x->getDefinitionPoint());
        o["text_pos"] = pt(x->getMiddleOfText());
        if (t == RS2::EntityDimLinear) {
            auto *d = static_cast<RS_DimLinear *>(e);
            o["p1"] = pt(d->getExtensionPoint1());
            o["p2"] = pt(d->getExtensionPoint2());
            o["angle"] = deg(d->getAngle());
            RS_Vector dir = RS_Vector::polar(1.0, d->getAngle());
            o["distance"] = std::abs(RS_Vector::dotP(d->getExtensionPoint2() - d->getExtensionPoint1(), dir));
        } else if (t == RS2::EntityDimAligned) {
            auto *d = static_cast<RS_DimAligned *>(e);
            o["p1"] = pt(d->getExtensionPoint1());
            o["p2"] = pt(d->getExtensionPoint2());
            o["distance"] = d->getExtensionPoint1().distanceTo(d->getExtensionPoint2());
        }
    }
    return o;
}

RS_Entity *findById(RS_Document *doc, const QString &id)
{
    for (RS_Entity *e : *doc)
        if (e && !e->isUndone() && QString::number(e->getId()) == id) return e;
    return nullptr;
}

// 範囲(bbox)が窓 [p1, p2] と重なるか
bool inWindow(RS_Entity *e, const RS_Vector &a, const RS_Vector &b, bool fully)
{
    RS_Vector lo(std::min(a.x, b.x), std::min(a.y, b.y)), hi(std::max(a.x, b.x), std::max(a.y, b.y));
    RS_Vector mn = e->getMin(), mx = e->getMax();
    if (fully) return mn.x >= lo.x && mn.y >= lo.y && mx.x <= hi.x && mx.y <= hi.y;
    return !(mx.x < lo.x || mn.x > hi.x || mx.y < lo.y || mn.y > hi.y);
}

// 描く図形に、指定の画層と色をつける。画層がなければ作る。
void applyAttrs(RS_Document *doc, RS_Entity *e, const QJsonObject &a)
{
    auto *g = static_cast<RS_Graphic *>(doc);
    if (a.contains("layer")) {
        const QString name = a.value("layer").toString();
        if (!g->getLayerList()->find(name)) g->addLayer(new RS_Layer(name));
        e->setLayer(name);
    } else {
        e->setLayerToActive();
    }
    e->setPenToActive();
    if (a.contains("color")) {
        RS_Pen p = e->getPen(false);
        p.setColor(RS_Color(QColor(a.value("color").toString())));
        e->setPen(p);
    }
}

QJsonObject addEntity(RS_Document *doc, RS_Entity *e, const QJsonObject &a)
{
    applyAttrs(doc, e, a);
    e->update();
    doc->addEntity(e);
    LC_UndoSection undo(doc);
    undo.addUndoable(e);
    refresh(doc);
    QJsonObject o = okObj();
    o["entity"] = entityJson(e, false);
    return o;
}

// 元の図形を複製して直し、元と入れ替える(元に戻せるようにするため)。
QJsonObject replaceEntity(RS_Document *doc, RS_Entity *org, RS_Entity *mod)
{
    mod->update();
    LC_UndoSection undo(doc);
    doc->addEntity(mod);
    undo.addUndoable(mod);
    if (org->isSelected()) org->setSelected(false);
    org->changeUndoState();
    undo.addUndoable(org);
    refresh(doc);
    QJsonObject o = okObj();
    o["entity"] = entityJson(mod, false);
    return o;
}

QSet<QString> liveIds(RS_Document *doc)
{
    QSet<QString> ids;
    for (RS_Entity *e : *doc)
        if (e && !e->isUndone()) ids.insert(QString::number(e->getId()));
    return ids;
}

// 操作の前後で、消えた id と増えた id を返す。LibreCAD は動かした図形を新しい図形に置き換えるため
void addIdChanges(QJsonObject &o, const QSet<QString> &before, const QSet<QString> &after)
{
    QJsonArray gone, added;
    for (const QString &k : before) if (!after.contains(k)) gone.append(k);
    for (const QString &k : after) if (!before.contains(k)) added.append(k);
    o["removed_ids"] = gone;
    o["new_ids"] = added;
}

// id の図形だけを選んだ状態にする。RS_Modification は選んだ図形に効くため。
int selectIds(RS_Document *doc, const QJsonArray &ids)
{
    QSet<QString> want;
    for (auto v : ids) want.insert(v.toString());
    int n = 0;
    for (RS_Entity *e : *doc) {
        if (!e || e->isUndone()) continue;
        bool on = want.contains(QString::number(e->getId()));
        e->setSelected(on);
        if (on) ++n;
    }
    return n;
}

RS2::LineType lineType(const QString &s)
{
    const QString k = s.toLower();
    if (k == "dash" || k == "dashed") return RS2::DashLine;
    if (k == "dot" || k == "dotted") return RS2::DotLine;
    if (k == "center") return RS2::CenterLine;
    if (k == "dashdot") return RS2::DashDotLine;
    if (k == "byblock") return RS2::LineByBlock;
    return RS2::SolidLine;
}

QStringList fontDirs()
{
    QStringList dirs;
    dirs << QDir::cleanPath(QCoreApplication::applicationDirPath() + "/../Resources/fonts");
    dirs << QStandardPaths::writableLocation(QStandardPaths::DocumentsLocation) + "/LibreCAD/fonts";
    return dirs;
}

QJsonObject docInfo(RS_Document *doc)
{
    auto *g = static_cast<RS_Graphic *>(doc);
    doc->calculateBorders();
    QJsonObject o = okObj();
    o["file"] = doc->getFilename();
    o["modified"] = g->isModified();
    o["insunits"] = g->getVariableInt("$INSUNITS", 0);
    o["unit"] = int(g->getUnit());
    o["extents"] = QJsonArray{pt(doc->getMin()), pt(doc->getMax())};
    o["dimtxt"] = g->getVariableDouble("$DIMTXT", 0);
    o["dimscale"] = g->getVariableDouble("$DIMSCALE", 1);
    o["dimasz"] = g->getVariableDouble("$DIMASZ", 0);
    o["dimlfac"] = g->getVariableDouble("$DIMLFAC", 1);
    QJsonObject counts;
    int n = 0;
    for (RS_Entity *e : *doc) {
        if (!e || e->isUndone()) continue;
        QString k = typeName(e->rtti());
        counts[k] = counts.value(k).toInt() + 1;
        ++n;
    }
    o["count"] = n;
    o["counts"] = counts;
    QJsonArray layers;
    for (RS_Layer *l : *g->getLayerList()) layers.append(l->getName());
    o["layers"] = layers;
    RS_Layer *al = g->getActiveLayer();
    o["current_layer"] = al ? al->getName() : "";
    QJsonArray blocks;
    for (int i = 0; i < g->getBlockList()->count(); ++i) blocks.append(g->getBlockList()->at(i)->getName());
    o["blocks"] = blocks;
    return o;
}

}  // namespace

QJsonObject lcHandle(const QJsonObject &req)
{
    const QString cmd = req.value("cmd").toString();
    const QJsonObject a = req.value("args").toObject();
    QJsonObject res = lcDispatch(cmd, a);
    QJsonObject entry;
    entry["t"] = QDateTime::currentDateTime().toString(Qt::ISODate);
    entry["cmd"] = cmd;
    entry["ok"] = res.value("ok").toBool();
    if (!entry["ok"].toBool()) entry["error"] = res.value("error");
    g_log.append(entry);
    while (g_log.size() > 500) g_log.removeFirst();
    return res;
}

QJsonObject lcDispatch(const QString &cmd, const QJsonObject &a)
{
    if (cmd == "ping") return okObj();

    // ---- ファイル(図面がなくても使える)
    if (cmd == "new") {
        auto *app = appWin();
        if (!app) return fail("no app window");
        g_docPath.clear();  // 新しい図面には名前がないので、前に戻す図面を忘れる
        app->slotFileNewNew();
        return docInfo(curDoc());
    }
    if (cmd == "open") {
        const QString path = QFileInfo(a.value("path").toString()).absoluteFilePath();
        if (!QFileInfo::exists(path)) return fail("file not found: " + path);
        auto *app = appWin();
        if (!app) return fail("no app window");
        app->slotFileOpen(path);
        g_docPath = path;
        RS_Document *d = curDoc();
        if (!d || QFileInfo(d->getFilename()).absoluteFilePath() != path) return fail("open failed");
        return docInfo(d);
    }
    if (cmd == "log") {
        QJsonObject o = okObj();
        o["log"] = g_log;
        return o;
    }
    if (cmd == "fonts") {
        QJsonArray arr;
        for (const QString &d : fontDirs())
            for (const QFileInfo &f : QDir(d).entryInfoList({"*.lff", "*.cxf"}, QDir::Files)) arr.append(f.baseName());
        QJsonObject o = okObj();
        o["fonts"] = arr;
        o["note"] = "日本語は unicode か kst32b。standard と kochigothic には漢字がない";
        return o;
    }

    RS_Document *doc = curDoc();
    if (!doc) return fail("no drawing is open");
    auto *g = static_cast<RS_Graphic *>(doc);

    // ---- 状態
    if (cmd == "doc_info") return docInfo(doc);

    if (cmd == "set_vars") {
        // 図面の設定を変える。例: {"$DIMTXT": 250, "$DIMASZ": 150, "$INSUNITS": 4}
        // 整数は group code 70、小数は 40、文字は 1 で入れる
        QJsonObject vars = a.value("vars").toObject();
        for (auto it = vars.begin(); it != vars.end(); ++it) {
            const QJsonValue v = it.value();
            if (v.isString()) g->addVariable(it.key(), v.toString(), 1);
            else if (v.isDouble() && v.toDouble() == std::floor(v.toDouble()) && it.key() != "$DIMTXT" &&
                     it.key() != "$DIMASZ" && it.key() != "$DIMSCALE" && it.key() != "$DIMEXE" &&
                     it.key() != "$DIMEXO" && it.key() != "$DIMGAP" && it.key() != "$DIMLFAC")
                g->addVariable(it.key(), v.toInt(), 70);
            else g->addVariable(it.key(), v.toDouble(), 40);
        }
        // 既にある寸法を、新しい設定で描き直す
        for (RS_Entity *e : *doc)
            if (e && !e->isUndone() && isDim(e->rtti())) static_cast<RS_Dimension *>(e)->updateDim();
        g->setModified(true);
        refresh(doc);
        return docInfo(doc);
    }
    if (cmd == "save") {
        if (doc->getFilename().isEmpty()) return fail("drawing has no file name; use save_as");
        if (!g->save()) return fail("save failed");
        QJsonObject o = okObj();
        o["path"] = doc->getFilename();
        return o;
    }
    if (cmd == "save_as") {
        const QString path = QFileInfo(a.value("path").toString()).absoluteFilePath();
        if (!path.endsWith(".dxf", Qt::CaseInsensitive)) return fail("path must end with .dxf");
        if (QFileInfo::exists(path) && !a.value("overwrite").toBool()) return fail("file exists (set overwrite=true)");
        if (!g->saveAs(path, RS2::FormatDXFRW, true)) return fail("save failed");
        g_docPath = path;
        QJsonObject o = okObj();
        o["path"] = path;
        return o;
    }

    // ---- 読み取り
    if (cmd == "list_entities") {
        const QString layer = a.value("layer").toString();
        QSet<QString> types;
        for (auto v : a.value("types").toArray()) types.insert(v.toString());
        const bool useWin = a.contains("window");
        RS_Vector w1, w2;
        if (useWin) {
            QJsonArray w = a.value("window").toArray();
            w1 = vec(w.at(0));
            w2 = vec(w.at(1));
        }
        const bool deep = a.value("expand_blocks").toBool();
        QJsonArray arr;
        for (RS_Entity *e : *doc) {
            if (!e || e->isUndone()) continue;
            RS_Layer *l = e->getLayer(true);
            if (!layer.isEmpty() && (!l || l->getName() != layer)) continue;
            if (!types.isEmpty() && !types.contains(typeName(e->rtti()))) continue;
            if (useWin && !inWindow(e, w1, w2, false)) continue;
            arr.append(entityJson(e, deep));
        }
        QJsonObject o = okObj();
        o["entities"] = arr;
        return o;
    }
    if (cmd == "get_entity") {
        RS_Entity *e = findById(doc, a.value("id").toString());
        if (!e) return fail("entity not found");
        QJsonObject o = okObj();
        o["entity"] = entityJson(e, true);
        return o;
    }
    if (cmd == "list_blocks") {
        QJsonArray arr;
        RS_BlockList *bl = g->getBlockList();
        for (int i = 0; i < bl->count(); ++i) {
            RS_Block *b = bl->at(i);
            QJsonObject o;
            o["name"] = b->getName();
            o["base"] = pt(b->getBasePoint());
            if (a.value("contents").toBool()) o["entities"] = childrenJson(b, false);
            else {
                int n = 0;
                for (RS_Entity *c : *b) if (c && !c->isUndone()) ++n;
                o["count"] = n;
            }
            int uses = 0;
            for (RS_Entity *e : *doc)
                if (e && !e->isUndone() && e->rtti() == RS2::EntityInsert && static_cast<RS_Insert *>(e)->getName() == b->getName()) ++uses;
            o["inserts"] = uses;
            arr.append(o);
        }
        QJsonObject o = okObj();
        o["blocks"] = arr;
        return o;
    }

    // ---- 描く
    if (cmd == "add_line")
        return addEntity(doc, new RS_Line(doc, vec(a.value("p1")), vec(a.value("p2"))), a);
    if (cmd == "add_point")
        return addEntity(doc, new RS_Point(doc, RS_PointData(vec(a.value("p")))), a);
    if (cmd == "add_circle")
        return addEntity(doc, new RS_Circle(doc, RS_CircleData(vec(a.value("center")), a.value("r").toDouble())), a);
    if (cmd == "add_arc") {
        // 角度は度。a1 から a2 へ反時計回り(reversed=true で時計回り)
        RS_ArcData d(vec(a.value("center")), a.value("r").toDouble(), rad(a.value("a1").toDouble()),
                     rad(a.value("a2").toDouble()), a.value("reversed").toBool());
        return addEntity(doc, new RS_Arc(doc, d), a);
    }
    if (cmd == "add_polyline") {
        auto *pl = new RS_Polyline(doc);
        for (auto v : a.value("points").toArray()) pl->addVertex(vec(v));
        if (a.value("closed").toBool()) pl->setClosed(true, 0.0);  // 2引数の版が、閉じる線分を足す
        return addEntity(doc, pl, a);
    }
    if (cmd == "add_text") {
        const QString h = a.value("align").toString("left");
        const QString v = a.value("valign").toString("baseline");
        RS_TextData::HAlign ha = h == "center" ? RS_TextData::HACenter : h == "right" ? RS_TextData::HARight
                               : h == "middle" ? RS_TextData::HAMiddle : RS_TextData::HALeft;
        RS_TextData::VAlign va = v == "middle" ? RS_TextData::VAMiddle : v == "top" ? RS_TextData::VATop
                               : v == "bottom" ? RS_TextData::VABottom : RS_TextData::VABaseline;
        RS_Vector p = vec(a.value("p"));
        RS_TextData d(p, p, a.value("height").toDouble(250), 1.0, va, ha, RS_TextData::None,
                      a.value("text").toString(), a.value("font").toString("unicode"),
                      rad(a.value("angle").toDouble(0)), RS2::Update);
        return addEntity(doc, new RS_Text(doc, d), a);
    }
    if (cmd == "add_dim_linear" || cmd == "add_dim_aligned") {
        // p1, p2 は測る2点。line は寸法線が通る点。angle は寸法線の向き(度、0 で水平、90 で垂直)
        RS_Vector p1 = vec(a.value("p1")), p2 = vec(a.value("p2")), at = vec(a.value("line"));
        RS_DimensionData dd(at, RS_Vector(false), RS_MTextData::VAMiddle, RS_MTextData::HACenter,
                            RS_MTextData::Exact, 1.0, a.value("text").toString(""), "Standard", 0.0);
        RS_Entity *dim;
        if (cmd == "add_dim_linear")
            dim = new RS_DimLinear(doc, dd, RS_DimLinearData(p1, p2, rad(a.value("angle").toDouble(0)), 0.0));
        else {
            // 平行寸法の定義点は、寸法線の上で p2 側の点。line を、p1-p2 に直交する向きに投影して求める
            RS_Vector n = (p2 - p1).normalized();
            n = RS_Vector(-n.y, n.x);
            dd.definitionPoint = p2 + n * RS_Vector::dotP(at - p1, n);
            dim = new RS_DimAligned(doc, dd, RS_DimAlignedData(p1, p2));
        }
        return addEntity(doc, dim, a);
    }
    if (cmd == "add_hatch") {
        // 閉じた境界(points)を塗る。pattern は SOLID か ANSI31 など
        const QString pattern = a.value("pattern").toString("SOLID");
        const bool solid = pattern.toUpper() == "SOLID";
        auto *h = new RS_Hatch(doc, RS_HatchData(solid, a.value("scale").toDouble(1), rad(a.value("angle").toDouble(0)), pattern));
        auto *loop = new RS_EntityContainer(h);
        loop->setPen(RS_Pen(RS2::FlagInvalid));
        QJsonArray pts = a.value("points").toArray();
        for (int i = 0; i < pts.size(); ++i)
            loop->addEntity(new RS_Line(loop, vec(pts.at(i)), vec(pts.at((i + 1) % pts.size()))));
        h->addEntity(loop);
        if (!h->validate()) { delete h; return fail("hatch boundary is not closed"); }
        return addEntity(doc, h, a);
    }
    if (cmd == "add_insert") {
        const QString name = a.value("block").toString();
        if (!g->getBlockList()->find(name)) return fail("block not found: " + name);
        RS_Vector sc = a.contains("scale") ? vec(a.value("scale")) : RS_Vector(1, 1);
        RS_InsertData d(name, vec(a.value("p")), sc, rad(a.value("angle").toDouble(0)), 1, 1, RS_Vector(0, 0), nullptr, RS2::Update);
        return addEntity(doc, new RS_Insert(doc, d), a);
    }
    if (cmd == "define_block") {
        // ids の図形を部品(ブロック)にする。replace=true なら、元の図形をその部品の挿入に置き換える
        const QString name = a.value("name").toString();
        if (name.isEmpty() || g->getBlockList()->find(name)) return fail("block name empty or exists");
        RS_Vector base = vec(a.value("base"));
        auto *blk = new RS_Block(doc, RS_BlockData(name, base, false));
        QList<RS_Entity *> src;
        for (auto v : a.value("ids").toArray()) {
            RS_Entity *e = findById(doc, v.toString());
            if (!e) { delete blk; return fail("entity not found: " + v.toString()); }
            src << e;
        }
        for (RS_Entity *e : src) {
            RS_Entity *c = e->clone();
            c->reparent(blk);
            blk->addEntity(c);
        }
        g->getBlockList()->add(blk);
        QJsonObject o = okObj();
        o["block"] = name;
        if (a.value("replace").toBool()) {
            LC_UndoSection undo(doc);
            for (RS_Entity *e : src) {
                e->setSelected(false);
                e->changeUndoState();
                undo.addUndoable(e);
            }
            auto *ins = new RS_Insert(doc, RS_InsertData(name, base, RS_Vector(1, 1), 0, 1, 1, RS_Vector(0, 0), nullptr, RS2::Update));
            ins->setLayerToActive();
            ins->setPenToActive();
            ins->update();
            doc->addEntity(ins);
            undo.addUndoable(ins);
            o["insert"] = entityJson(ins, false);
        }
        refresh(doc);
        return o;
    }

    // ---- 直す
    if (cmd == "set_props") {
        RS_Entity *e = findById(doc, a.value("id").toString());
        if (!e) return fail("entity not found");
        RS_Entity *c = e->clone();
        if (a.contains("layer")) {
            const QString name = a.value("layer").toString();
            if (!g->getLayerList()->find(name)) g->addLayer(new RS_Layer(name));
            c->setLayer(name);
        }
        if (a.contains("color")) {
            RS_Pen p = c->getPen(false);
            p.setColor(RS_Color(QColor(a.value("color").toString())));
            c->setPen(p);
        }
        if (a.contains("text")) {
            const QString t = a.value("text").toString();
            if (c->rtti() == RS2::EntityText) static_cast<RS_Text *>(c)->setText(t);
            else if (c->rtti() == RS2::EntityMText) static_cast<RS_MText *>(c)->setText(t);
            else if (isDim(c->rtti())) static_cast<RS_Dimension *>(c)->setLabel(t);
            else { delete c; return fail("text can be set only on text, mtext, dimension"); }
        }
        if (a.contains("height")) {
            if (c->rtti() == RS2::EntityText) static_cast<RS_Text *>(c)->setHeight(a.value("height").toDouble());
            else if (c->rtti() == RS2::EntityMText) static_cast<RS_MText *>(c)->setHeight(a.value("height").toDouble());
        }
        if (c->rtti() == RS2::EntityLine && (a.contains("p1") || a.contains("p2"))) {
            auto *l = static_cast<RS_Line *>(c);
            if (a.contains("p1")) l->setStartpoint(vec(a.value("p1")));
            if (a.contains("p2")) l->setEndpoint(vec(a.value("p2")));
        }
        if (isDim(c->rtti())) static_cast<RS_Dimension *>(c)->updateDim(true);
        return replaceEntity(doc, e, c);
    }
    if (cmd == "move" || cmd == "copy" || cmd == "rotate" || cmd == "scale" || cmd == "mirror" || cmd == "delete") {
        const QSet<QString> before = liveIds(doc);
        int n = selectIds(doc, a.value("ids").toArray());
        if (n == 0) return fail("no entity matched ids");
        RS_Modification m(*doc, curView());
        bool ok = true;
        const bool copy = cmd == "copy" || a.value("keep_original").toBool();
        if (cmd == "move" || cmd == "copy") {
            RS_MoveData d;
            d.number = copy ? 1 : 0;
            d.offset = vec(a.value("offset"));
            ok = m.move(d);
        } else if (cmd == "rotate") {
            RS_RotateData d;
            d.number = copy ? 1 : 0;
            d.center = vec(a.value("center"));
            d.angle = rad(a.value("angle").toDouble());
            ok = m.rotate(d);
        } else if (cmd == "scale") {
            RS_ScaleData d;
            d.number = copy ? 1 : 0;
            d.referencePoint = vec(a.value("center"));
            double f = a.value("factor").toDouble(1);
            d.factor = RS_Vector(f, f);
            ok = m.scale(d);
        } else if (cmd == "mirror") {
            RS_MirrorData d;
            d.copy = copy;
            d.axisPoint1 = vec(a.value("p1"));
            d.axisPoint2 = vec(a.value("p2"));
            ok = m.mirror(d);
        } else {
            m.remove();
        }
        doc->setSelected(false);
        refresh(doc);
        QJsonObject o = ok ? okObj() : fail(cmd + " failed");
        o["count"] = n;
        addIdChanges(o, before, liveIds(doc));
        return o;
    }
    if (cmd == "stretch") {
        // 窓 [p1, p2] の中にある端点を offset だけ動かす。壁を動かすと、寸法や窓も一緒に伸び縮みする
        const QSet<QString> before = liveIds(doc);
        RS_Modification m(*doc, curView());
        bool ok = m.stretch(vec(a.value("p1")), vec(a.value("p2")), vec(a.value("offset")));
        refresh(doc);
        QJsonObject o = ok ? okObj() : fail("stretch failed");
        addIdChanges(o, before, liveIds(doc));
        return o;
    }
    if (cmd == "undo" || cmd == "redo") {
        int n = a.value("steps").toInt(1), done = 0;
        for (int i = 0; i < n; ++i) {
            bool r = cmd == "undo" ? doc->undo() : doc->redo();
            if (!r) break;
            ++done;
        }
        refresh(doc);
        QJsonObject o = okObj();
        o["steps"] = done;
        o["note"] = "undo/redo のあとは id が変わる。list_entities で取り直す";
        return o;
    }

    // ---- 画層
    if (cmd == "layers") {
        QJsonArray arr;
        for (RS_Layer *l : *g->getLayerList()) {
            QJsonObject o;
            o["name"] = l->getName();
            o["color"] = l->getPen().getColor().name();
            o["linetype"] = int(l->getPen().getLineType());
            o["visible"] = !l->isFrozen();
            o["locked"] = l->isLocked();
            arr.append(o);
        }
        QJsonObject o = okObj();
        o["layers"] = arr;
        RS_Layer *al = g->getActiveLayer();
        o["current"] = al ? al->getName() : "";
        return o;
    }
    if (cmd == "set_layer") {
        // 画層を作るか直す。current=true で今の画層にする
        const QString name = a.value("name").toString();
        if (name.isEmpty()) return fail("name is empty");
        RS_Layer *l = g->getLayerList()->find(name);
        if (!l) {
            l = new RS_Layer(name);
            g->addLayer(l);
        }
        RS_Pen p = l->getPen();
        if (a.contains("color")) p.setColor(RS_Color(QColor(a.value("color").toString())));
        if (a.contains("linetype")) p.setLineType(lineType(a.value("linetype").toString()));
        l->setPen(p);
        if (a.contains("visible")) l->freeze(!a.value("visible").toBool());
        if (a.value("current").toBool(false)) g->activateLayer(l);
        g->getLayerList()->setModified(true);
        refresh(doc);
        return okObj();
    }

    // ---- 確かめる
    if (cmd == "zoom") {
        RS_GraphicView *v = curView();
        if (!v) return fail("no view");
        if (a.contains("window")) {
            QJsonArray w = a.value("window").toArray();
            v->zoomWindow(vec(w.at(0)), vec(w.at(1)));
        } else {
            v->zoomAuto();
        }
        return okObj();
    }
    if (cmd == "screenshot") {
        // 図面を映す部分だけを PNG にする。window を渡すと、その範囲を映してから撮る
        RS_GraphicView *v = curView();
        QWidget *w = curViewWidget();
        if (!v || !w) return fail("no view");
        if (a.contains("window")) {
            QJsonArray win = a.value("window").toArray();
            v->zoomWindow(vec(win.at(0)), vec(win.at(1)));
        } else if (a.value("fit").toBool(true)) {
            v->zoomAuto();
        }
        v->redraw();
        QApplication::processEvents();
        QPixmap px = w->grab();
        const QString path = QFileInfo(a.value("path").toString()).absoluteFilePath();
        if (!path.endsWith(".png", Qt::CaseInsensitive)) return fail("path must end with .png");
        if (!px.save(path, "PNG")) return fail("could not write png");
        QJsonObject o = okObj();
        o["path"] = path;
        o["size"] = QJsonArray{px.width(), px.height()};
        return o;
    }

    return fail("unknown cmd: " + cmd);
}
