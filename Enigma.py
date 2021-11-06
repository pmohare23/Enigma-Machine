def rotate(el,val): eval(rotors[el])[0]=eval(rotors[el])[0][val:]+eval(rotors[el])[0][:val]; pos[el]+=val   #Rotar spin calculation

def convert(text,converted=""):
  for ch in text:
    if ch.isalpha():
      if chr(pos[-2]+65) in eval(rotors[-2])[1:]: rotate(-3,1),rotate(-2,1) #Medium Rotor Notch Triggerred (Double Mechanism - Slow & Medium Rotors)
      elif chr(pos[-1]+65) in eval(rotors[-1])[1:]: rotate(-2,1)            #Fast Rotor Notch Trigger & Medium Rotor Spin
      rotate(-1,1); offset=[0]+pos[::-1]; path=rotors[::-1]+[reflector]     #Fast Rotor Spin
      for i in range(len(path)): ch=(eval(path[i])[0])[(ord(ch)-65-offset[i])%26]                           #Forward Current from Rotors to Reflector (RL)
      for i in range(len(rotors)): ch=chr((eval(rotors[i])[0]).index(chr(((ord(ch)-65+pos[i])%26)+65))+65)  #Reverse Current from Reflector (LR)    
    converted+=ch
  return converted                                                          #Output to Lampboard

def plugboard(text): return ''.join((Plug[Plug.index(ch)+1] if Plug.index(ch)%3==0 else Plug[Plug.index(ch)-1]) if ch in Plug and ch!=" " else ch for ch in text)

def setup():
  start=(input("Start Positions (A-Z/1-26) [ "+" ".join(rotors)+" ] : ").upper()).split()                   #Start Position (Grundstellung)
  if start!=[]:
    if len(rotors)!=len(start): exit("Invalid Start Configuration")
    for el in range(len(rotors)): rotate(el,int(start[el])-1 if start[el].isdigit() else ord(start[el])-65)
  ring=(input("Ring Position (A-Z/1-26) [ "+" ".join(rotors)+" ] : ").upper()).split()                      #Ring Setting (Ringstellung)
  if ring!=[]:
    if len(rotors)!=len(ring): exit("Invalid Ring Configuration")
    for el in range(len(rotors)):
      val=int(ring[el])-1 if ring[el].isdigit() else ord(ring[el])-65
      eval(rotors[el])[0]=''.join(chr(((ord(lp)-65+val)%26)+65) for lp in (eval(rotors[el])[0][-val:]+eval(rotors[el])[0][:-val]))

val,rotors,ref,rot,pos=False,[],[],[],[0,0,0]; Plug="BQ CR DI EJ KW MT OS PX UZ GH" #Init Variables & Plugboard default configuration with 10 cables (Steckerbrett)
if input("---ENIGMA---\nCurrent Plugboard: "+Plug+"\nReconfigure Plugboard? (Y/N): ") in ('Y','y'): Plug=(input("New Plugboard Configuration (A-Z): ")).upper()
for i in range(len(Plug)): val=True if (i%3!=2 and Plug[i]==" ") or (i%3==2 and Plug[i]!=" ") else val      #Plugboard validation
exit("Invalid Plugboard Connection") if (len(set(Plug.replace(' ',''))))!=len(Plug.replace(' ','')) or val else print("Plugboard:",Plug)
mach=input("Select mach Type (Enigma 1/M3/M4): ").upper()
print("\n---"+("Kriegsmarine M3" if mach in ("2","M3") else "Kriegsmarine M4" if mach in ("3","M4") else "Enigma 1")+"---")
Rotor_1=["EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"]            #Y notch              #Single Notch Wheel with Turnover in window
Rotor_2=["AJDKSIRUXBLHWTMCQGZNPYFVOE","E"]            #M notch
Rotor_3=["BDFHJLCPRTXVZNYEIWGAKMUSQO","V"]            #D notch
Rotor_4=["ESOVPZJAYQUIRHXLNFTGKDCMWB","J"]            #R notch
Rotor_5=["VZBRGITYUPSDNHLXAWMJQOFECK","Z"]            #H notch
if mach in ("2","3","M3","M4"):                                             #Dual Notch Wheel (M3/M4)
  Rotor_6=["JPGVOUMFYQBENHZRDKASXLICTW","Z","M"]      #H,U notch
  Rotor_7=["NZJHGRCXMYSWBOUFAIVLPEKQDT","Z","M"]      #H,U notch
  Rotor_8=["FKQHTLXOCBJSPDZRAMEWNIUYGV","Z","M"]      #H,U notch
if mach in ("3","M4"):                                                      #Beta & Gamma Rotors - for M4 only
  Rotor_Beta=["LEYJVCNIXWPBQMDRTAKZGFUHOS"]
  Rotor_Gamma=["FSOKANUERHMBTIYCWLQPZXVGJD"]
  Reflector_Thin_B=("ENKQAUYWJICOPBLMDXZVFTHRGS",)                          #Thin-Reflector (Umkehrwalze) - for M4 only
  Reflector_Thin_C=("RDOBJNTKVEHMLFCWZAXGYIPSUQ",)
else:
  Reflector_A=("EJMZALYXVBWFCRQUONTSPIKHGD",)                               #Reflector (Umkehrwalze)
  Reflector_B=("YRUHQSLDPXNGOKMIEBFZCWVJAT",)
  Reflector_C=("FVPJIAOYEDRZXWGCTKUQSBNMHL",)                                                  
for i in list(globals()): rot.append(i) if "Rotor_" in i else ref.append(i) if "Reflector_" in i else None  #Catalog available Rotors & Reflectors
if mach in ("3","M4"):
  rot4=input("Rotors (Beta/Gamma):").lower()
  rotors=[rot[-2]] if rot4 in ("1","beta") else [rot[-1]] if rot4 in ("2","gamma") else exit("Invalid Rotor"); rot=rot[:-2]; pos.append(0)
rotors+=[rot[int(i)-1] for i in input("Rotors: "+" ".join(rot)+"\nSelect 3 Rotors (1-"+str(len(rot))+"): ").split()]  #Rotors Selection & Validation
if (mach in ("3","M4") and len(set(rotors))!=4) or (mach not in ("3","M4") and len(set(rotors))!=3): exit("Invalid Number of Rotors")
reflector=ref[int(input("Reflectors: "+" ".join(ref)+"\nSelect a Reflector (1-"+str(len(ref))+"): "))-1]              #Reflector Selection
if input("Setup Rotors (Y/N): ") in ('Y','y'): setup()              #Setup Start & Ring Position of Rotor
print(plugboard(convert(plugboard(input("Input string to encode/decode (A-Z): ").upper()))))
