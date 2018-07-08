from array import array
import sys

def h(k):
    if k == 1:
        return array('l', [ 2, 4 ])
    else:
        a = h(k-1)
        a.append(3*a[k-1] - a[k-2])
        return a

def go(h, k, n):
    # 1. Draw G^{k,n}
    # 1a. draw the glues
    print("""\\draw[ultra thick, xgreen](1,0.5)--({:f},0.5)--
             ({:f},1.5)--({:f},1.5)--({:f},2);"""
          .format(n+0.5, n+0.5, n-0.5, n-0.5))
    # 1b. draw the tiles
    for i in range(1, n+1):
        print("\\drawg{{{:d}}}{{0}}".format(i))
    print("\\drawg{{{:d}}}{{1}}\\drawg{{{:d}}}{{1}}".format(n, n-1))

    # 2. Draw O^{k,n}
    # 2a. draw the glues
    print("\\draw[ultra thick, xorange]({:f},2)--({:f},{:f});"
          .format(n-0.5, n-0.5, h[k]))
    for i in range(1,k+1):
        print("\\draw[ultra thick, xorange]({:f}, {:f})--({:f}, {:f});"
              .format(n-0.5, h[i]-0.5, n, h[i]-0.5))
    # 2b. draw the tiles
    for i in range(2, h[k]):
        print("\\drawo{{{:d}}}{{{:d}}}".format(n-1, i))


def br(h, k, n):
    # 1. Draw B^{k,n}
    # 1a. draw the glues
    print("""\\draw[ultra thick, xblue]({:f},{:f})--({:f},{:f})--
          ({:f},{:f})--({:f},{:f})--({:f},{:f});"""
          .format(n, h[k]-0.5, 2*n-0.5, h[k]-0.5, 2*n-0.5,
                  h[k]-1.5, n+0.5, h[k]-1.5, n+0.5, h[k]-2))

    # 1b. draw the tiles
    for b in range(n, 2*n):
        print("\\drawb{{{:d}}}{{{:d}}}\\drawb{{{:d}}}{{{:d}}}"
              .format(b, h[k]-1, b, h[k]-2))

    # 2. Draw R^{k,n}
    # 2a. draw the glues
    print("\\draw[ultra thick, xred]({:f},{:f})--({:f},{:f});"
          .format(n+0.5, h[k]-2, n+0.5, h[k-1]))
    for i in range(2,k+1):
        print("\\draw[ultra thick, xred]({:f}, {:f})--({:f}, {:f});"
              .format(n+0.5, h[k] - (h[i]-h[i-1])+0.5,
                      n+1, h[k] - (h[i]-h[i-1])+0.5))
    # 2b. draw the tiles
    for r in range(h[k-1], h[k]-2):
        print("\\drawr{{{:d}}}{{{:d}}}".format(n, r))

def p(h, k, n):
    print("%% {} {}".format(k,n))
    if k > 0:
        # Draw G^{k,n} and O^{k,n}
        go(h, k, n)
        # For all east glues on O^{k,n}
        for i in range(1,k+1):
            # Draw B^{i,n} and R^{i,n}
            br(h, i, n)
            # Attach all appropriate translations to R^{i,n}.
            for j in range(1,i):
                print("\\begin{{scope}}[shift={{({:d},{:d})}}]"
                      .format(n, h[i] - (h[j+1]-h[j])))
                p(h, j, n)
                print("\\end{scope}")

def path(k, n):
    print("""\\documentclass[class=minimal,border=0pt]{standalone}
\\usepackage{tikz}\\definecolor{xgreen}{RGB}{0,128,0}
\\definecolor{xblue}{RGB}{0,204,255}
\\definecolor{xorange}{RGB}{255,165,0}
\\definecolor{xred}{RGB}{255,0,0}
\\newcommand{\\draws}[2]{\\draw[fill=white](#1.16,#2.16)rectangle(#1.84,#2.84);}
\\newcommand{\\drawg}[2]{\\draw[fill=xgreen](#1.16,#2.16)rectangle(#1.84,#2.84);}
\\newcommand{\\drawo}[2]{\\draw[fill=xorange] (#1.16,#2.16)rectangle(#1.84,#2.84);}
\\newcommand{\\drawb}[2]{\\draw[fill=xblue] (#1.16,#2.16)rectangle(#1.84,#2.84);}
\\newcommand{\\drawr}[2]{\\draw[fill=xred] (#1.16,#2.16)rectangle(#1.84,#2.84);}""")

    hh = h(k)
    print("""\\begin{{document}}\\begin{{tikzpicture}}
          \\clip (-1, -1) rectangle ({:f},{:f});"""
          .format(n * (k+1)+1, hh[k] + 1))
    print("\\draw[ultra thick](0.5,0.5)--(1, 0.5);\\draws{0}{0}")
    p(hh, k, n)
    print("\\end{tikzpicture}\\end{document}")

path(int(sys.argv[1]), int(sys.argv[2]))
