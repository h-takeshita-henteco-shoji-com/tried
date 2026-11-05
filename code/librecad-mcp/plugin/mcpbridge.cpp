// 1行1件の JSON で命令を受け、1行1件の JSON で返す。命令の中身は lc_ops.cpp。
// 窓口を開いている間は QEventLoop で待つ。窓は modal にしないので、人も同時に図面を触れる。
#include "mcpbridge.h"
#include "document_interface.h"
#include "lc_ops.h"

#include <QApplication>
#include <QDialog>
#include <QEventLoop>
#include <QJsonDocument>
#include <QLabel>
#include <QPushButton>
#include <QTcpServer>
#include <QTcpSocket>
#include <QVBoxLayout>
#include <QWidget>

static const quint16 kPort = 7471;

QString LC_McpBridge::name() const { return "MCP bridge"; }

PluginCapabilities LC_McpBridge::getCapabilities() const
{
    PluginCapabilities caps;
    caps.menuEntryPoints << PluginMenuLocation("plugins_menu", "MCP bridge");
    return caps;
}

QJsonObject LC_McpBridge::handle(Document_Interface *doc, const QJsonObject &req)
{
    Q_UNUSED(doc);  // 図面は、命令ごとに本体の画面から今のものを取り直す(開く・新規のあとも追えるように)
    return lcHandle(req);
}

void LC_McpBridge::execComm(Document_Interface *doc, QWidget *parent, QString cmd)
{
    Q_UNUSED(cmd);
    QDialog dlg(parent);
    dlg.setWindowTitle("MCP bridge");
    auto *lay = new QVBoxLayout(&dlg);
    auto *label = new QLabel(&dlg);
    auto *count = new QLabel("受けた命令: 0", &dlg);
    auto *stop = new QPushButton("止める", &dlg);
    lay->addWidget(label);
    lay->addWidget(count);
    lay->addWidget(stop);

    QTcpServer server;
    if (!server.listen(QHostAddress::LocalHost, kPort)) {
        label->setText("待ち受けできません: " + server.errorString());
    } else {
        label->setText(QString("127.0.0.1:%1 で待ち受け中").arg(kPort));
    }
    int n = 0;
    QObject::connect(&server, &QTcpServer::newConnection, [&]() {
        while (QTcpSocket *s = server.nextPendingConnection()) {
            QObject::connect(s, &QTcpSocket::disconnected, s, &QObject::deleteLater);
            QObject::connect(s, &QTcpSocket::readyRead, [&, s]() {
                while (s->canReadLine()) {
                    QJsonParseError err;
                    QJsonDocument in = QJsonDocument::fromJson(s->readLine(), &err);
                    QJsonObject out;
                    if (err.error != QJsonParseError::NoError || !in.isObject()) {
                        out["ok"] = false;
                        out["error"] = "bad json";
                    } else {
                        out = handle(doc, in.object());
                        out["id"] = in.object().value("id");
                    }
                    s->write(QJsonDocument(out).toJson(QJsonDocument::Compact) + "\n");
                    s->flush();
                    count->setText(QString("受けた命令: %1").arg(++n));
                }
            });
        }
    });

    // 窓は modal にしない。人も同時に図面を触れる。
    QEventLoop loop;
    QObject::connect(stop, &QPushButton::clicked, &dlg, &QDialog::close);
    QObject::connect(&dlg, &QDialog::finished, &loop, &QEventLoop::quit);
    dlg.setModal(false);
    dlg.show();
    loop.exec();
    server.close();
}
