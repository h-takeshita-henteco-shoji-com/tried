// LibreCAD の plugin。図面の操作を 127.0.0.1 の TCP で受け付け、MCP server(../server.py)から使えるようにする。
#ifndef MCPBRIDGE_H
#define MCPBRIDGE_H

#include "qc_plugininterface.h"
#include <QObject>
#include <QJsonObject>

class LC_McpBridge : public QObject, QC_PluginInterface
{
    Q_OBJECT
    Q_INTERFACES(QC_PluginInterface)
    Q_PLUGIN_METADATA(IID LC_DocumentInterface_iid FILE "mcpbridge.json")

public:
    PluginCapabilities getCapabilities() const override;
    QString name() const override;
    void execComm(Document_Interface *doc, QWidget *parent, QString cmd) override;

private:
    QJsonObject handle(Document_Interface *doc, const QJsonObject &req);
};

#endif
