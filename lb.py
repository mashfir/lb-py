import os
import datetime
import re
import subprocess


def get_input():
    title = input("enter title of post: ")
    filename = clean_filename(title)
    publish_date = datetime.datetime.now().strftime("%b. %d, %Y")
    h_publish_date = "<h4>{}</h4>\n".format(publish_date)
    h_title = "<h1>{}</h1>\n".format(title)
    subprocess.call(["vim", "posts/.drafts/" + filename])

    return filename, h_title, h_publish_date


def clean_filename(title: str):
    fname = re.sub(r"[^a-z0-9\s]+", "", title.lower())
    fname = re.sub(r"\s+", "-", fname) + ".html"
    return fname


def read_boilerplate():
    header = open(os.path.join("templates/", "header.html"), "r").read()
    footer = open(os.path.join("templates/", "footer.html"), "r").read()
    return header, footer


def main():
    fname, title, date = get_input()
    post = open(os.path.join("posts/.drafts/", fname), "r").read()
    header, footer = read_boilerplate()
    with open(os.path.join("posts/", fname), "w") as f:
        f.write(header + title + date + post + footer)
        f.close()


if __name__ == "__main__":
    main()
