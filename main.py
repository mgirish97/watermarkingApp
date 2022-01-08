from tkinter import *
from tkinter import filedialog, font, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw


global my_image, canvas, canvas_image, image_filename
global input_text, text_win
global new_image, out


window = Tk()
window.config(padx=50, pady=50)
window.title('Watermarking Tool')


MY_FONT = font.Font(family="Verdana", size=18)


def open_image():
    """Connected to add_photo_button. Lets you choose a photo from local files and then displays it."""
    global add_photo_button, watermark_button
    global my_image, canvas, canvas_image, image_filename
    window.filename = filedialog.askopenfilename(title='Select a File',
                                                 filetypes=(("JPEG files", "*.jpeg"),))
    my_image = ImageTk.PhotoImage(file=window.filename)
    image_filename = window.filename

    canvas = Canvas(width=my_image.width(), height=my_image.height())
    canvas_image = canvas.create_image(round(my_image.width()/2), round(my_image.height()/2), image=my_image)
    add_photo_button.grid_forget()
    canvas.grid(padx=20, pady=20, row=0, column=0)
    watermark_button.grid(row=1, column=0)


def input_watermark_text():
    """Connected to watermark_button. Opens a new window to ask for input text for watermark."""
    global input_text, text_win
    text_win = Toplevel()
    text_win.title('Watermark Text')
    text_win.config(padx=50, pady=50)
    input_label = Label(text_win, text='What would you like your watermark text to be?', font=('Gill Sans', 25))
    input_label.config(padx=20, pady=20)
    input_label.pack()
    input_text = Entry(text_win, width=10)
    input_text.pack()
    add_text_button = Button(text_win, text='Add Text', height=2, width=12, command=add_watermark)
    add_text_button['font'] = MY_FONT
    add_text_button.pack(pady=20)


def add_watermark():
    """Connected to add_text_button in input_watermark_text function. Alpha composites the given text
    on the selected image and displays the watermarked image on original window."""
    global new_image, out
    watermark_button.grid_forget()
    with Image.open(image_filename).convert('RGBA') as im:
        txt = Image.new("RGBA", im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        image_font = ImageFont.truetype('Verdana.ttf', size=30)
        draw.text((round(im.width/2) - 50, round(im.height/2)), text=input_text.get(),
                  fill=(255, 255, 255, 128), font=image_font)
        text_win.destroy()
        out = Image.alpha_composite(im, txt)
        new_image = ImageTk.PhotoImage(image=out)
        canvas.itemconfig(canvas_image, image=new_image)
    save_photo_button.grid(row=1, column=0)


def save_photo():
    """Connected to save_photo_button. Opens dialog box to save photo to local directory."""
    if messagebox.askokcancel(title='Watermarking Tool', message='Would you like to save your photo?'):
        out.save('watermarked_image.png')
    canvas.grid_forget()
    save_photo_button.grid_forget()
    add_photo_button.grid(row=1, column=1)


add_photo_button = Button(text="Add Image", height=2, width=12, command=open_image)
add_photo_button['font'] = MY_FONT
add_photo_button.grid(row=1, column=1)

watermark_button = Button(text='Add Watermark', height=2, width=15, command=input_watermark_text)
watermark_button['font'] = MY_FONT

save_photo_button = Button(text='Save Photo?', height=2, width=15, command=save_photo)
save_photo_button['font'] = MY_FONT


window.mainloop()

