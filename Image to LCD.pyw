from PIL import Image
from time import sleep
from tkinter import Tk, Frame, Entry, LabelFrame, Button, Label,StringVar
from tkinter import filedialog
import tkinter.font as tkFont



def TFTcolor(r, g, b):
    return (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3))

def getPixVals(img, w, h):
    im = Image.open(img)
    pix = im.load()
    rgbvals = []
    for b in range(h):
        for i in range(w):
            rgbvals.append((TFTcolor(pix[i, b][0], pix[i, b][1], pix[i, b][2])))
    return tuple(rgbvals)

def getPixValsTXT(img, w, h):
    im = Image.open(img)
    dataname = img.split(".")
    fi = open(f'{dataname[0]}.txt', "a")
    pix = im.load()
    for b in range(h):
        for i in range(w):
            fi.write(str((hex(TFTcolor(pix[i, b][0], pix[i, b][1], pix[i, b][2])))))
            if b*i != w*h:
                fi.write("\n")
    fi.close()

def getPixValsTXT_HEX(img):
    im = Image.open(img)
    w, h = im.size
    dataname = img.split(".")
    fi = open(f'{dataname[0]}.h', "a")
    pix = im.load()
    fi.write(f'#ifndef {img.split(".")[0].upper()}_H\n#define {img.split(".")[0].upper()}_H\n#include <stdint.h>\n#include <pgmspace.h>\nconst uint16_t {dataname[0]}[{w*h}] = ')
    fi.write("{")
    for b in range(h):
        for i in range(w):
            fi.write(str((hex(TFTcolor(pix[i, b][0], pix[i, b][1], pix[i, b][2])))))
            if (b+1)*(i+1) == w*h:
                fi.write("};\n#endif")
            else:
                fi.write(", ")

    fi.close()


def openFile():
    filename = filedialog.askopenfilename()
    data = filename.split("/")
    global name
    name = data[len(data)-1]
    textBox.config(text=f'"{name}" selected.')

def convert():
    getPixValsTXT_HEX(str(name))
    print("16-bit pixel values succesfully created!")
    sleep(1)
    window.destroy()


window = Tk()
window.geometry("340x230+850+400")
window.title("Image to LCD")
window.resizable(False, False)
window.config(background="#1c1c1c",)
helv16 = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)
helv8 = tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD)

frame = Frame(window)
frame.config(pady=15, background="#1c1c1c")
frame.pack()

labelText = StringVar(window)
labelText.set("Test")

#widthTextFrame = LabelFrame(frame, font=helv8, text="Enter width")
#widthTextFrame.grid(row=0, column=0, padx=10, pady=10)
#widthTextFrame.config(borderwidth=0)

#widthBox=Entry(widthTextFrame)
#widthBox.grid(row=0, column=0)


#heightTextFrame = LabelFrame(frame,font=helv8,text="Enter height")
#heightTextFrame.grid(row=0, column=2, padx=10, pady=10)
#heightTextFrame.config(borderwidth=0)

#heightBox=Entry(heightTextFrame)
#heightBox.grid(row=0, column=0,)

button = Button(frame, text="Choose file", width= 20, height=2, borderwidth=5, font=helv16, command = openFile)
button.config(bg='green')
button.grid(column=1, pady=5)

textBox = Label(frame, text="Select your image...", font=("Arial", 10, ),fg="#ffffff", background="#1c1c1c")
textBox.grid(column=1)

exitBTN = Button(frame, text="Convert", width= 20, height=2, borderwidth=5, font=helv16, command = convert)
exitBTN.config(bg='#ff412b')
exitBTN.grid(column=1, pady=20)


window.mainloop()

