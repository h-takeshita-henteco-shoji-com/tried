// 命令を受けて、LibreCAD の図面を操作する(lc_ops.cpp)。
#ifndef LC_OPS_H
#define LC_OPS_H
#include <QJsonObject>
#include <QString>

// 命令を1つ処理し、記録に残す
QJsonObject lcHandle(const QJsonObject &req);
// 命令を1つ処理する(記録はしない)
QJsonObject lcDispatch(const QString &cmd, const QJsonObject &args);
#endif
