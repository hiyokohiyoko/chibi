import pegpy.tpeg as pegpy
peg = pegpy.grammer('chibi.tpeg')
parser = pegpy.generate(peg)

def sun(s: str):
    pass

def main():
    s = input('>>>')
    run(s)

if __name__ == '__main__':
    main()