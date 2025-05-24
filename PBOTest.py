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

def load_tugas(filename="tugas_data.txt"):
    tugas_list = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.read().split("--------------------------\n")
            for entry in lines:
                if entry.strip():
                    parts = entry.strip().split("\n")
                    if len(parts) >= 4:
                        judul = parts[0]
                        deskripsi = parts[1]
                        deadline = parts[2]
                        status = parts[3] == "True"
                        tugas_obj = tugas(judul, deskripsi, deadline, status)
                        tugas_list.append(tugas_obj)
    except FileNotFoundError:
        pass
    return tugas_list

def save_all_tugas(tugas_list, filename="tugas_data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for tugas_obj in tugas_list:
            f.write(f"{tugas_obj.judul}\n{tugas_obj.deskripsi}\n{tugas_obj.deadline}\n{tugas_obj.status}\n--------------------------\n")

def add_tugas(tugas_obj, filename="tugas_data.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{tugas_obj.judul}\n{tugas_obj.deskripsi}\n{tugas_obj.deadline}\n{tugas_obj.status}\n--------------------------\n")

def sorting_tugas_deadline(tugas_list):
    return sorted(
        tugas_list, key=lambda t: datetime.strptime(str(t.deadline), '%d-%m-%Y %H:%M') if isinstance(t.deadline, str) else t.deadline
    )




