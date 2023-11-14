from tkinter import *
from tkinter import ttk

from reportlab.pdfgen import canvas

#custom font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics 

pdfmetrics.registerFont(
    TTFont("calibri", "calibrib.ttf" )
)



root = Tk()

class FuncPDF():
     
    def Base(self,pdf,x_start, y_start,x_end,y_end):
        pdf.line(x_start,y_start,x_end,y_start) #linhas horizontais
        pdf.line(x_start,y_end,x_end,y_end)     #   

        pdf.line(x_start,y_start,x_start,y_end) #linhas verticais
        pdf.line(x_end,y_end,x_end,y_start)     #

    def Text(self,pdf,y_pos,nomecliente, nf, transportadora, volume_counter ,volume_total):
        
        pdf.drawCentredString(294,y_pos, f"{nomecliente}")
        pdf.drawCentredString(294,y_pos - 50, f"NF: {nf} - {transportadora}")
        pdf.drawCentredString(294,y_pos - 100 , f"VOLUME: {volume_counter}/{volume_total}")

    def generator(self, nomecliente, nf,transportadora ,volumes):
        base_start_x = 40 #imutavel, sempre será
        base_start_y = 820
        base_end_x = 555 #imutavel, sempre será
        base_end_y = 650
        self.pdf = canvas.Canvas(f"ETIQUETA {nomecliente}.pdf")
        self.pdf.setFont("calibri", 36)
        BASE_subtractor = 210
        TEXT_subtractor = 40
        count = 0
        if len(nomecliente) > 27:
            raise Exception("O nome do cliente não pode ter mais que 27 caracteres.")

        for x in range(int(volumes)):

            if count == 4:
                self.pdf.showPage()
                self.pdf.setFont("calibri", 36)
                count = 0
                base_start_x = 40 #imutavel, sempre será
                base_start_y = 820
                base_end_x = 555 #imutavel, sempre será
                base_end_y = 650

            self.Base(self.pdf,base_start_x, base_start_y, base_end_x, base_end_y)
            self.Text(self.pdf,base_start_y - TEXT_subtractor, nomecliente, nf, transportadora, x+1, volumes )
            base_start_y -= BASE_subtractor
            base_end_y -= BASE_subtractor
            count += 1
        self.pdf.save() 
    
    def digest_jamef(self):
        self.nomecliente = self.nome_entry.get()
        self.nf = self.nf_entry.get()
        self.volumes = self.volume_entry.get()

        global nomeCli
        nomeCli = self.nomecliente

        self.generator(self.nomecliente,self.nf,"JAMEF",self.volumes)

        self.volume_entry.delete(0, END)
        self.nf_entry.delete(0, END)
        self.nome_entry.delete(0,END)


    
    def digest_acredite(self):
        self.nomecliente = self.nome_entry.get()
        self.nf = self.nf_entry.get()
        self.volumes = self.volume_entry.get()

        self.generator(self.nomecliente,self.nf,"ACREDITE LOG",self.volumes)

        self.volume_entry.delete(0, END)
        self.nf_entry.delete(0, END)
        self.nome_entry.delete(0,END)

class Application(FuncPDF):
    def __init__(self):
        self.root = root
        self.Tela()
        self.Frame()
        self.Widgets()
        root.mainloop()
    
    def Tela(self):
        self.root.title("Sistema de Etiquetas")
        self.root.geometry("400x250")
        self.root.resizable(False,False)
    
    def Frame(self):
        self.frame = Frame(self.root,bg="white")
        self.frame.place(relx=0.0, rely=0.0,relwidth=1,relheight=1)
    
    def Widgets(self):

        #label nome cliente
        self.nome_label = Label(self.frame, text="Nome do Cliente")
        self.nome_label.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.1)

        #entry
        self.nome_entry = Entry(self.frame)
        self.nome_entry.place(relx=0.1, rely=0.2, relwidth=0.5, relheight=0.1)

        #label nf
        self.nf_label = Label(self.frame, text="Nota Fiscal")
        self.nf_label.place(relx=0.1, rely=0.35, relwidth=0.2, relheight=0.1)

        #entry
        self.nf_entry = Entry(self.frame)
        self.nf_entry.place(relx=0.1, rely=0.45, relwidth=0.2, relheight=0.1)

        #label volumes
        self.volume_label = Label(self.frame, text="Volumes")
        self.volume_label.place(relx=0.40, rely=0.35, relwidth=0.2, relheight=0.1)

        #entry
        self.volume_entry = Entry(self.frame)
        self.volume_entry.place(relx=0.40, rely=0.45, relwidth=0.2, relheight=0.1)

         #botao de gerar etiqueta
        self.jamef_bt = Button(self.frame, text="JAMEF",bg="red",font=("verdana", 8, "bold"), command=self.digest_jamef)
        self.jamef_bt.place(relx= 0.1, rely=0.65, relwidth=0.3, relheight=0.1)
        
         
        self.acredite_bt = Button(self.frame, text="ACREDITE",bg="yellow", font=("verdana", 8, "bold"), command=self.digest_acredite)
        self.acredite_bt.place(relx= 0.5, rely=0.65, relwidth=0.3, relheight=0.1)






Application()