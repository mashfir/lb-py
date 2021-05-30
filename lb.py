from html import HTML

def main():
    h = HTML()
    title = input("enter title of post: ")
    h_title = h.h1(title)
    print("title is: " + title)
    print("Marked up title is: " + h_title)


if __name__ == "__main__":
    main()
