class File_System:
    def __init__(self, file_system_name, block_size, amount_of_blocks):
        self.system = file_system_name
        self.block_size = block_size
        self.amount_of_blocks = amount_of_blocks

    def create(self):
        with open(self.system, mode='w') as my_system:
            for _ in range(self.amount_of_blocks):
                my_system.write("0" * self.block_size + "\n")

    def data_to_massive_ready_for_system(self, data):
        temporary = str()
        for i in data:
            temporary += str(i) + " "

        temporary_massive = []
        n = self.block_size - 1
        for i in range(0, len(temporary), n):
            temporary_massive.append(temporary[i:i + n])

        return temporary_massive

    def get_system_data(self):
        with open(self.system, encoding="utf-8", mode='r') as my_system:
            system_data = my_system.readlines()
        return system_data

    def check_for_free_space(self, all_data, processed_data):
        free_space_counter = 0
        for i in all_data:
            if i[0] == "0":
                free_space_counter += 1
        processed_data_size = len(processed_data)
        if free_space_counter >= processed_data_size + 1:
            return True
        else:
            return False

    def add_file(self, name, data):
        processed_data = self.data_to_massive_ready_for_system(data)
        all_data = self.get_system_data()
        enough_space = self.check_for_free_space(all_data, processed_data)

        if enough_space:
            for i in range(len(all_data)):
                if all_data[i][0] == "0":
                    all_data[i] = "#" + name + " " + ((self.block_size - (len(name) + 2)) * "0") + "\n"
                    break

            counter = 0
            for i in range(len(all_data)):
                if all_data[i][0] == "0":
                    all_data[i] = "/" + processed_data[counter] + (
                            (self.block_size - (len(processed_data[counter]) + 1)) * "0"
                    ) + "\n"

                    if counter != len(processed_data) - 1:
                        counter += 1
                    else:
                        break

            with open(self.system, encoding="utf-8", mode='w') as my_system:
                my_system.writelines(all_data)
        else:
            print("Недостаточно места")

    def delete_file(self, name):
        all_data = self.get_system_data()
        delete_massive = []

        for i in range(len(all_data)):
            if all_data[i].startswith("#" + name):
                delete_massive.append(i)

        try:
            for i in range(delete_massive[0] + 1, len(all_data)):
                if all_data[i][0] == "/":
                    delete_massive.append(i)
                else:
                    break
        except IndexError:
            print("Файл не найден")

        for i in delete_massive:
            all_data[i] = "0" * self.block_size + "\n"

        with open(self.system, encoding="utf-8", mode='w') as my_system:
            my_system.writelines(all_data)

    def read_file(self, name):
        all_data = self.get_system_data()
        read_massive = []

        for i in range(len(all_data)):
            if all_data[i].startswith("#" + name):
                read_massive.append(i)

        try:
            for i in range(read_massive[0] + 1, len(all_data)):
                if all_data[i][0] == "/":
                    read_massive.append(i)
                else:
                    break
        except IndexError:
            print("Файл не найден")

        text = str()
        for i in read_massive[1:]:
            text += all_data[i][1:-1]
        print(text)

    def copy_file(self, name):
        all_data = self.get_system_data()
        copy_massive = []

        for i in range(len(all_data)):
            if all_data[i].startswith("#" + name):
                copy_massive.append(i)

        try:
            for i in range(copy_massive[0] + 1, len(all_data)):
                if all_data[i][0] == "/":
                    copy_massive.append(i)
                else:
                    break
        except IndexError:
            print("Файл не найден")

        enough_space = self.check_for_free_space(all_data, copy_massive[1:])

        counter = 0
        try:
            if enough_space:
                for i in range(len(all_data)):
                    if all_data[i][0] == "0":
                        all_data[i] = all_data[copy_massive[counter]]
                        counter += 1
                        if counter == len(copy_massive):
                            break
            else:
                print("Недостаточно места")
        except IndexError:
            pass

        with open(self.system, encoding="utf-8", mode='w') as my_system:
            my_system.writelines(all_data)

    def sort(self):
        all_data = self.get_system_data()
        empty_block_massive = []

        for i in range(len(all_data)):
            if all_data[i][0] == "0":
                empty_block_massive.append(i)

        empty_block_massive.sort(reverse=True)
        for i in empty_block_massive:
            all_data.pop(i)
            all_data.append(str("0" * 64 + "\n"))

        with open(self.system, encoding="utf-8", mode='w') as my_system:
            my_system.writelines(all_data)


class File:
    def __init__(self):
        self.name = str()
        self.data = []

    def create(self):
        name = str(input("Название файла: "))
        self.name = name
        while True:
            data = str(input(""))
            if data == "":
                print("Ввод завершён\n")
                break
            self.data.append(data)


def main():
    system = File_System("my_file_system.fs", 64, 8)
    # system.create()

    # file_01 = File()
    # file_01.create()
    # system.add_file(file_01.name, file_01.data)

    # system.delete_file("text.txt")
    system.read_file("test.txt")
    # system.copy_file("test.txt")
    # system.sort()


if __name__ == '__main__':
    main()
