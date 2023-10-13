from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb
from tkinter import messagebox
from math import log10, sqrt
import numpy as np 
from skimage.metrics import structural_similarity as ssim
from Cryptography import Cryptography
import Huffman as hff
import pickle
root=Tk()
root.title("Secure Transmission - Hide an Encrypted Data in an Image")
root.geometry("700x600+150+90")
root.resizable(False,False)
root.configure(bg="#2f4155")

obj=Cryptography(1024)

def showimage():
    global filename
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                        title='Select Image File',
                                        filetype=(("JPG file", "*.jpg"),
                                                  ("PNG file","*.png"),
                                                  ("All file","*.txt")))
    img=Image.open(filename)
    img=ImageTk.PhotoImage(img)
    lb1.configure(image=img,width=250,height=250)
    lb1.image=img

def save():
    split = os.path.splitext(filename)
    index=len(split)-1
    newfile = split[0] + "_stego.png"
    secret.save(newfile)
    messagebox.showinfo("Save", "Stego Image Saved Successfully")


global s
def Hide():
    global secret
    # global Tree
    msg=text1.get(1.0,END)
    msg=msg.replace("\n","|")
    cipher,n=obj.encrypt(msg)
    key = str(obj.get_private_key())
    msgcon = cipher + "--" + key + "--" + str(n)
    Tree,s=hff.buildHuffmanTree(msgcon)
    print("Huffman Object : ",Tree)
    with open("Huffman.pickle", "wb") as f:
        pickle.dump(Tree, f)
    #print("private key\n"+key)
    #print("Cipher Text\n"+ cipher)
    #print("Messageconcatenation "+msgcon)
    #print(msgcon)
    message="$"+s+"$"
    if len(message) == 1:
        messagebox.showinfo("Hide", "Please enter Text...")
    else:
        secret = lsb.hide(str(filename),message)
        # Message Box
        print("Embeded Message: "+message)
        messagebox.showinfo("Hide", "Data Hide Successfully")
    split = os.path.splitext(filename)
    index=len(split)-1
    newfile = split[0] + "_stego.png"
    secret.save(newfile)
    messagebox.showinfo("Save", "Stego Image Saved Successfully")
    print("Calculations: ")
    original_file=filename
     #Stego Image
    stegano_file=newfile

    # load the images and convert them to grayscale
    imgA = Image.open(original_file).convert('L')
    imgB = Image.open(stegano_file).convert('L')

    print(original_file)
    print(stegano_file)

    # convert the images to numpy arrays
    imgA = np.array(imgA)
    imgB = np.array(imgB)

    # calculate the MSE between the two images
    mse = np.mean((imgA - imgB) ** 2)

    #PSNR Callculation
    if (mse == 0):  # MSE is zero means no noise is present in the signal .
          # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))

    # Calculate the SSIM
    ssim_value = ssim(imgA, imgB, multichannel=True)

    Label(frame6, text=str(len(message)), bg="#2f4155", font="Times 12 bold", fg="white").place(x=20, y=5)
    Label(frame6, text=str(mse), bg="#2f4155", font="Times 12 bold", fg="white").place(x=100, y=5)
    Label(frame6, text=str(psnr), bg="#2f4155", font="Times 12 bold", fg="white").place(x=300, y=5)
    Label(frame6, text=str(ssim_value), bg="#2f4155", font="Times 12 bold", fg="white").place(x=500, y=5)

    print("MSE: %.2f, SSIM: %.2f" % (mse, ssim_value))


def Show():
    clear_message = lsb.reveal(filename)
    #print("Embeded Message "+clear_message)
    print("Added Message "+clear_message)
    clear_message=clear_message.replace("$","")
    #Open the file to get the pickle value
    with open("Huffman.pickle", "rb") as f:
        Tree = pickle.load(f)
    clear_message=hff.decodeValues(Tree,clear_message)
    print("Decoded Message "+clear_message)
    emdmsg=clear_message.split("--")
    cipher,privkey,n=emdmsg
    print("All Values",emdmsg)
    plain = obj.customDecrypt(cipher,int(privkey),int(n))
    plain = plain.replace("|","\n")
    print("Decrypted Message: ",plain)
    text1.delete(1.0,END)
    text1.insert(END,plain)
#icon
image_icon=PhotoImage(file="favicon.png")
root.iconphoto(False,image_icon)

#logo
logo=PhotoImage(file="logo.png")
Label(root,image=logo,bg="#2f4135").place(x=10,y=0)
Label(root,text="Secure Transmission",bg="#2d4155",fg="white",font="arial 25 bold").place(x=100,y=20)

#first Frame
f=Frame(root,bg="black",width=340, height=280, relief=GROOVE)
f.place(x=10,y=80)

lb1=Label(f,bg="black")
lb1.place(x=40,y=10)

#Secomd Frame
frame2=Frame(root,bd=3,width=340,height=280,bg="white",relief=GROOVE)
frame2.place(x=350,y=80)

text1=Text(frame2,font="Times 20",bg="white",fg="black",relief=GROOVE,wrap=WORD)
text1.place(x=0,y=0,width=320,height=295)

scrollbar1=Scrollbar(frame2)
scrollbar1.place(x=320,y=0,height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#third Frame
frame3=Frame(root,bd=3,bg="#2f4155",width=330, height=100,relief=GROOVE)
frame3.place(x=10,y=370)

Button(frame3,text="Open Image",width=10,height=2,font="Times 14 bold",command=showimage).place(x=20,y=30)
Button(frame3,text="Save Image",width=10,height=2,font="Times 14 bold",command=save).place(x=180,y=30)
Label(frame3,text="Picture, Image, Photo File",bg="#2f4155",fg="yellow").place(x=20,y=5)

#fourth Frame
frame4=Frame(root,bd=3,bg="#2f4155",width=330, height=100,relief=GROOVE)
frame4.place(x=360,y=370)

Button(frame4,text="Hide Data",width=10,height=2,font="Times 14 bold",command=Hide).place(x=20,y=30)
Button(frame4,text="Show Data",width=10,height=2,font="Times 14 bold",command=Show).place(x=180,y=30)
Label(frame4,text="Picture, Image, Photo File",bg="#2f4155",fg="yellow").place(x=20,y=5)


#Fifth Frame
frame5=Frame(root,bd=3,bg="#2f4155",width=680, height=100,relief=GROOVE)
frame5.place(x=10,y=480)
Label(frame5, text="Parametters for RSA", bg="#2f4155", fg="yellow").place(x=20, y=5)
Label(frame5, text="MSG Len", bg="#2f4155", font="Times 12", fg="white").place(x=20, y=30)
Label(frame5, text="MSE", bg="#2f4155", font="Times 12", fg="white").place(x=100, y=30)
Label(frame5, text="PSNR", bg="#2f4155", font="Times 12", fg="white").place(x=300, y=30)
Label(frame5, text="SSIM", bg="#2f4155", font="Times 12", fg="white").place(x=500, y=30)

#Sixth Frame
frame6=Frame(root,bd=2,bg="#2f4155",width=680, height=50,relief=GROOVE)
frame6.place(x=10,y=540)

root.mainloop()
