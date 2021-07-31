from datetime import datetime


def read_file(file_name):
    f = open(file_name, 'r')
    values = f.readlines()
    return values

def write_to_log(string):
    time = datetime.now().strftime('%d/%m/%Y %H:%M')
    string = time + ': ' + string

    # Open the file in append & read mode ('a+')
    with open("log.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(string)