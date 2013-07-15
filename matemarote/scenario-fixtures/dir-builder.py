# Debe existir matemarote/matemarote/scenario-fixtures/../media/games/avioncito/v1.0.5.1 con un juego andando

real_game = {"game": 1, "version": "1.0.5.1",}
dirs = [#{"game": 1, "version": "1.0.5.1",},
{"game": 2, "version": "1.0.5.1",},
{"game": 3, "version": "1.0.5.1",},
{"game": 1, "version": "1.0.5.2",},
{"game": 3, "version": "1.0.5.2",},

{"game": 1, "version": "1.0.3.1",},
{"game": 3, "version": "1.0.3.1",},
{"game": 2, "version": "1.0.3.1",},
{"game": 1, "version": "1.0.3.2",},
{"game": 3, "version": "1.0.3.2",},

{"game": 3, "version": "1.0.4.1",},
{"game": 1, "version": "1.0.4.1",},
{"game": 2, "version": "1.0.4.1",},
{"game": 1, "version": "1.0.4.2",},
{"game": 3, "version": "1.0.4.2",},
{"game": 1, "version": "1.0.4.4",},
]

g = {1: "avioncito", 2: "memomarote", 3: "casitas"}

import os

base = os.path.abspath(os.path.dirname(__file__))
media = os.path.join(base, '../media/games')

real_game_path = os.path.join(os.path.join(media, g[1]), "v"+real_game["version"])
        
print real_game_path

for (k,v) in g.items():
    directory = os.path.join(media, v)
    print directory
    if not os.path.exists(directory):
        os.makedirs(directory)
        print "No existe"
    else:
        print "Existe"

for i in dirs:
    current_game_path = os.path.join(os.path.join(media, g[i["game"]]), "v"+i["version"])
    print current_game_path, 
    if not os.path.exists(current_game_path):
        os.symlink(real_game_path, current_game_path)        
        print "  No existe"
    else:
        print "  Existe"
#~ os.symlink(src, os.path.join(dst, os.path.dirname(src)))        
