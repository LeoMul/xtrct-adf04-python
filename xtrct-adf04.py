import argparse
import sys
CM2RYD=109737.43

def find_cs(path,upper,lower):
    f = open(path,'r')
    readin = f.readlines()
    length = len(readin)
    for jj in range(0,length):
        current_line = readin[jj]
        #print(current_line)
        if current_line.split()[0] == '-1':
            break
    if jj > (length-1):
        print("error, does your file have the -1 after the energies? that is what i'm looking for")
        return 
    num_levels = jj - 2

    e1 = float(readin[lower].split()[-1])
    e2 = float(readin[upper].split()[-1])
    diff = (e2-e1) / CM2RYD
    #print(diff)
    temps = readin[jj+1].split()[2:]

    for ii in range(jj+2,length):
        current_line = readin[ii]
        current_line = current_line.split()
        if current_line[0] == '-1':
            print("ran off end of file, is your upper too big?")
            exit()
        
        #print(current_line)

       

        if int(current_line[0]) == upper or int(current_line[0]) == lower:
             if int(current_line[1]) == upper or int(current_line[1]) == lower:
                 print("Found transition")
                 break
    if ii > (length-1):
        print("didnt find transition, check adf04 or user input")
        return
    collision_strengths = current_line[3:]
    #print(temps)
    return temps,collision_strengths,diff

def write_out(upper,lower,temps,collisions,diff,filename):
    f = open(filename,'w')
    upp = max(upper,lower)
    low = min(upper,lower)
    header = "#eff cs. trans:" + str(upp) + ' -- ' + str(low) + " E_ij = " + str(round(diff,7)) + " Ry\n"
    f.write(header)
    for jj in range(0,len(temps)):
        temps[jj] = temps[jj].replace('+','E+').replace('-','E-')
        collisions[jj]=collisions[jj].replace('+','E+').replace('-','E-')
    #print(header)
    for jj in range(0,len(temps)):
        string_to_be_written = temps[jj] + " " + collisions[jj] + "\n"
        #print(string_to_be_written)
        f.write(string_to_be_written)
    f.close()

def main(path,upper,lower,filename):
    temps,collision_strengths,diff = find_cs(path,upper,lower)
    write_out(upper,lower,temps,collision_strengths,diff,filename)

parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument('-n', '--name',  help='Specify desired file name. Leave blank for default: "your adf04 name"_extracted_upper_lower')
parser.add_argument('-f', '--adf04', help='Paths of adf04')
parser.add_argument('-l', '--lower', help='lower index')
parser.add_argument('-u', '--upper', help='upper index')

args = parser.parse_args()

if not len(sys.argv) > 1:
    print("you didnt give me anything, showing help")
    parser.print_help()
    exit()

if not args.adf04:
    print("no adf04 file supplied.")
    exit() 
elif not args.upper:
    print("no upper level supplied")
    exit()
elif not args.lower:
    print("no lower level supplied")
    exit()
else:
    lower = int(args.lower)
    upper = int(args.upper)
    if args.name:
        file_name = args.name
    else:
        file_name = args.adf04+"_extracted_"+str(max(upper,lower))+"_"+str(min(upper,lower))
    
    if lower == upper:
        print("upper and lower the same, stopping")
        exit()
    else:
        main(args.adf04,upper,lower,file_name)