# ChessWithWong

"一起下棋吧"小游戏APL-git版

# 打包成.EXE方法

cd ...\ChessWithWong

pyinstaller -F -w ChesswithWong.py ai.py colour.py functions.py piece.py settings.py usercontrol.py
