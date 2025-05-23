from datetime import datetime
class tugas:
    def __init__ (self, judul, deskripsi, deadline, status):
        self.judul = judul
        self.deskripsi = deskripsi
        self.deadline = deadline
        self.status = status
        
    
    # Method Setter
    def set_Judul(self, judul):
        self.judul = judul

    def set_Deskripsi(self, deskripsi):
        self.deskripsi = deskripsi

    def set_Deadline(self, deadline):
        self.deadline = deadline

    def set_Status(self, status):
        self.status = status

    # Method Getter
    def get_Judul(self):
        return self.judul
    
    def get_Deskripsi(self):
        return self.deskripsi 
    
    def get_Deadline(self):
        return self.deadline
    
    def get_Status(self):
        return self.status


    # method
    def TambahTugas(self):
        input_judul = input(self.judul)
        input_deskripsi = input(self.deskripsi)
        input_deadline = datetime.strptime(input(self.deadline), '%d-%m-%Y %H:%M') 
        input_status = False    
        
        tugas_baru = tugas(input_judul, input_deskripsi, input_deadline, input_status)
        with open('tugas.txt', 'a') as f:
            f.write(f"{tugas_baru.judul}, {tugas_baru.deskripsi}, {tugas_baru.deadline}, {tugas_baru.status}\n")    
        
    def EditTugas(self):
        with open('tugas.txt', 'r') as f:
            lines = f.readlines()
        
        with open('tugas.txt', 'w') as f: 
            for line in lines:
                if line.startswith(self.judul):
                    line = f"{self.judul}, {self.deskripsi}, {self.deadline}\n"
                f.write(line)

    def tandaiSelesai(self):
        self.status = True
        
    def HapusTugas(self):
        print("Placeholder for HapusTugas method")

    def LihatSemuaTugas(self):
        print("Placeholder for LihatSemuaTugas method")
        
    def SortingTugas(self):
        with open('tugas.txt', 'r') as f:
            lines = f.readlines()
        
        lines.sort(key=lambda x: datetime.strptime(x.split(',')[2], '%d-%m-%Y %H:%M'))





