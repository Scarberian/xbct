import colorsys
from flask import abort, flash, Flask, g,\
        render_template, render_template_string,\
        request, session, url_for
import ipdb
from itertools import cycle
from multiprocessing import Process
import time
import sqlite3
import webbrowser

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
DEEP=True
#48bit - Default bit depth (Deep Color)
BASE=16
ABBUND = 32

def pallygen(base=BASE):
    colors = []
    kj = base**5
    ki = base**4
    k = base**3
    j = base**2
    for a in range(base) :
        for c in range(base) :
            for e in range(base) :
                colors.append('#' + str(hex(a*(kj+1)+c*(ki+base)+ e*(k+j)))[2:].rjust(6, '0').upper())
    return colors

def forty8(triad):
    """(list of 3tuples) -> list of 3tupels
    return a new version of triad that is translated from
    24bit to 48 bit.
    >>>forty8('#FFFFFF','#005500', '#e0e0e0')
    ('#FFFFFFFFFFFF', '#000055550000', '#E0E0E0E0E0E0')
    """

#    ipdb.set_trace()
    def bitter(rgb24):
        """(str) -> str
        return 48bit color hexes from a triad of 24bit ones
        >>> bitter('#FFFFFF')
        #FFFFFFFFFFFF
        """

        def deeper(t):
            """(str)->(str,str,str)
            >>> splitter('#FFFFFF')
            ['FF', 'FF', 'FF']
            """

            def mirror(bit):
                """(str)->str
                return a switch bit from 8 deep to 16
                >>> mirror('FF')
                'FFFF'
                """
                x = int(bit,16)
                return str(hex(x*256+x))[2:].rjust(4,'0')

            return "".join([mirror(i) for i in t[1:3],t[3:5],t[5:7]])
        return deeper(rgb24)
    return ['#' + bitter(i) for i in triad]

def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
    return colorsys.rgb_to_hsv(r, g, b)

def triads(spin=BASE**3/3):
    color_gen = cycle(pallygen())
    palette = {}

    for i in range(BASE**3):
        this = color_gen.next()
        palette[get_hsv(this)] = this
    hues = sorted(palette)

    pallys = cycle([palette[x] for x in hues])
    p0 = [pallys.next() for i in xrange(spin)]
    p1 = [pallys.next() for i in xrange(spin)]
    p2 = [pallys.next() for i in xrange(spin)]
    h0 = cycle(p0+p1+p2)
    h1 = cycle(p1+p2+p0)
    h2 = cycle(p2+p0+p1)
    return [(h0.next(),h1.next(),h2.next()) for i in xrange(BASE**3)]

app = Flask(__name__)
#app.config.from_object('__name__.default.settings')
app.config.from_envvar('XBCT_SETTINGS', silent=True)
@app.route("/")
def index():
    print "NEW REQUEST>>", time.time()
    if DEEP:
        colors = [forty8(triads()[i]) for i in xrange(0,BASE**3,BASE**3/ABBUND)]
    colors = [triads()[i] for i in xrange(0,BASE**3,BASE**3/ABBUND)]
    html = '''<html lang="en">
<head>
    <title>Hex colors</title>
</head>
<body>
Triads are horizontal,
gradient is vertical
    <table border="1">
        <tr>
            <th>--------Hex--------</th>
            <th>--------Color--------</th>
            <th>--------Hex--------</th>
            <th>--------Color--------</th>
            <th>--------Hex--------</th>
            <th>--------Color--------</th>
        </tr>
    {% for color in colors %}
        <tr>
            <td>{{color[0]}}</td>
            <td style="background-color:{{color[0]}}"></td>
            <td>{{color[1]}}</td>
            <td style="background-color:{{color[1]}}"></td>
            <td>{{color[2]}}</td>
            <td style="background-color:{{color[2]}}"></td>
        </tr>
    {% endfor %}
    </table>
</body>
</html>'''
    return render_template_string(html, colors=colors)

def tabber():
    time.sleep(1)
    webbrowser.open_new_tab("http://127.0.0.1:5000")

if __name__ == "__main__":
    p = Process(target=tabber)
    p.start()
    app.run(debug=True)
#    ipdb.set_trace()
#000000000000       #000055550000       #0e0e0000e0e0   
#a1a155551a1a       #1616cccc6161       #6d6d0000d6d6   
#b5b5aaaa5b5b       #3d3dffffd3d3       #bdbd1111dbdb   
#848499994848       #383877778383       #ecec4444cece   
#6363aaaa3636       #070733337070       #c5c500005c5c   
#bbbbffffbbbb       #8c8c8888c8c8       #c2c222222c2c   
#5757bbbb7575       #8e8e5555e8e8       #e8e8aaaa8e8e   
#2929cccc9292       #bdbd6666dbdb       #e1e1aaaa1e1e   
#080888888080       #dddd0000dddd       #a0a0aaaa0a0a   
#2f2f9999f2f2       #dcdcbbbbcdcd       #a4a4ffff4a4a   
#171722227171       #f4f422224f4f       #6565bbbb5656   
#6e6e4444e6e6       #fafabbbbafaf       #ababffffbaba   
#9e9e2222e9e9       #c5c599995c5c       #151588885151   
#666644446666       #d9d9dddd9d9d       #aeaeeeeeeaea   
#ebeb5555bebe       #b5b5eeee5b5b       #5b5b9999b5b5   
#a5a533335a5a       #7474eeee4747       #8f8faaaaf8f8   
