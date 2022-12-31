def main():
  _dict = read()
  print(_dict)

def read() -> dict:
    _dict = {}
    try:
        with open("Homework\\Lesson (08.12)\\http.txt") as file:
            for line in file.readlines() : 
                key, *value = line.replace("\n","").replace(" ","").split(":")
                _dict[key] = value
        return _dict
    except OSError as err: 
        print("read:", err)



if __name__ == "__main__" :
    main()