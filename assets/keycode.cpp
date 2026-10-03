// SPDX-License-Identifier: GPL-3.0-only
#include <QCoreApplication>
#include <QKeySequence>
#include <QTextStream>
int main(int argc,char**argv){QCoreApplication a(argc,argv);QTextStream o(stdout);for(int i=1;i<argc;i++){auto k=QKeySequence(QString::fromUtf8(argv[i]));o<<(k.isEmpty()?0:k[0].toCombined())<<"\n";}}
