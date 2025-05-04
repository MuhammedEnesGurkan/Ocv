#Bu kod opencvden alınan görüntüleri tkinter'da ekranda gösterebilmek için pil kütüphanesi aracılığıyla tkimage'a çevirir ve ardından canvasta gösterir.
import cv2
import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
cap = None
def main():

    ekran = ctk.CTk()
    ekran.geometry("800x600")
    ekran.title("kamera")
    ekran.minsize(800,600)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    def video_baslat():
        global cap  # Global değişken olarak tanımla

        # Kamera bağlantısı oluştur
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Kamera açılamadı!")
            return

        # İlk kare görüntüsünü al ve video güncelleme fonksiyonunu başlat
        video_guncelle()

    def video_guncelle():
        """bu kod kamera açıksa görünütüyü alır ve opencvnin numpy dizisi şeklinde aldığı görüntüyü
        PIL image'a çevirir ve tkinter canvas'a ekler"""
        global cap

        if cap and cap.isOpened():
            ret, frame = cap.read()

            if ret:
                # BGR'den RGB'ye dönüştür
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Boyutu ayarla
                resized_frame = cv2.resize(rgb_frame, (640, 480))

                # PIL Image'a dönüştür
                pil_img = Image.fromarray(resized_frame)

                # Tkinter PhotoImage'a dönüştür
                tk_img = ImageTk.PhotoImage(image=pil_img)

                # Canvas'ı temizle
                video_canvas.delete("all")

                # Canvas'a görüntüyü ekle (x=0, y=0 sol üst köşe)
                video_canvas.create_image(0, 0, image=tk_img, anchor="nw")

                # Referansı tut (önemli!)
                video_canvas.image = tk_img

            # 30ms sonra tekrar çağır (yaklaşık 30 FPS)
            ekran.after(30, video_guncelle)
        else:
            # Kamera açık değilse mesaj göster
            video_canvas.delete("all")
            video_canvas.create_text(320, 240, text="Kamera bağlı değil", fill="black")




    def video_durdur():
        global cap

        if cap and cap.isOpened():
            cap.release()
            video_canvas.delete("all")
            video_canvas.create_text(320, 240, text="Kamera durduruldu", fill="black")
            cap=None
        else:
            video_canvas.delete("all")
            video_canvas.create_text(320, 240, text="Kamera zaten durduruldu", fill="black")


    #butonları ekle
    video_start_buton = ctk.CTkButton(ekran,text="video_baslat",command=video_baslat)
    video_start_buton.grid(row=0,column=0,padx=5,pady=5,sticky="ew")

    video_stop_buton = ctk.CTkButton(ekran,text="Video Durdur",command=video_durdur)
    video_stop_buton.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    video_canvas = tkinter.Canvas(ekran, width=640, height=480)
    video_canvas.grid(row=0,column=3,padx=10,pady=5,sticky="ew")



    #10 msde bir ekran güncelleme
    ekran.after(10,video_guncelle)
    ekran.mainloop()

if __name__ == "__main__":
    main()

