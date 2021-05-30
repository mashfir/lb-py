import os

def main():
    title = input("enter title of post: ")
    h_title = "<h1>{}</h1>\n".format(title)
    header = open(os.path.join("templates/", "header.html"), "r").read()
    footer = open(os.path.join("templates/", "footer.html"), "r").read()
    print(header + h_title + footer)

if __name__ == "__main__":
    main()
