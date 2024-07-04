HEADERS = []

src = open("wiringpi.i").read().split('\n')

for line in src:
    line = line.strip()
    if line.startswith('#include') and line.endswith('.h"'):
        HEADERS.append(line.replace('#include','').replace('"','').strip())

#print(HEADERS)

def is_c_decl(line):
    for fn in ['wiringPiISR','wiringPiSetupPiFace','wiringPiSetupPiFaceForGpioProg']:
        if fn in line:
            if 'wiringPiISRStop' in line:
                return True
            else:
                return False
    for prefix in ['extern','void','int','uint8_t']:
        if line.startswith(prefix):
            return True

print("// Generated by generate-bindings.py - do not edit manually!")

for file in HEADERS:
    print("\n// Header file {}".format(file))
    h = open(file).read().split('\n')
    extern = False
    cont = False
    if 'extern "C" {' not in h:
        extern = True
    for line in h:
        line = line.strip()
        if 'UNU' in line[-5:]:
            line = line[:-5] + ';'
        if cont:
            print("\t{}".format(line))
            cont = ";" not in line
            continue
        if line.startswith('extern "C"'):
            extern = True
            continue
        if is_c_decl(line) and extern:
            print(line)
            cont = ";" not in line
