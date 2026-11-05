# LibreCAD 2.2.1(Qt 5.15)向けの plugin。build の手順は ../README.md
QT       += gui widgets network
TEMPLATE = lib
CONFIG += plugin c++17
TARGET = mcpbridge
QMAKE_MACOSX_DEPLOYMENT_TARGET = 11.0

# 本体のソース(v2.2.1)。plugin の API と、本体の内部の header を使う
LIBRECAD_SRC = $$(LIBRECAD_SRC)
LC = $$LIBRECAD_SRC/librecad/src
INCLUDEPATH += $$LC/plugins $$LC/lib/engine $$LC/lib/debug $$LC/lib/math $$LC/lib/gui \
               $$LC/lib/modification $$LC/lib/information $$LC/lib/creation $$LC/lib/fileio \
               $$LC/lib/actions $$LC/lib/filters $$LC/main $$LC/ui $$LC/ui/generic \
               $$LIBRECAD_SRC/libraries/libdxfrw/src
# 本体と同じ定義にそろえる(部品の大きさがずれないように)
DEFINES += DWGSUPPORT MUPARSER_STATIC

# 本体の内部の関数は、LibreCAD の実行ファイルが読み込まれたときにつながる
QMAKE_LFLAGS += -undefined dynamic_lookup

SOURCES += mcpbridge.cpp lc_ops.cpp
HEADERS += mcpbridge.h lc_ops.h
