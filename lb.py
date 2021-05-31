import os
import datetime
import re
import subprocess
import csv
import sys


def get_input():
    title = input("enter title of post: ")
    filename = clean_filename(title)
    add_new_post(title, filename)
    publish_date = datetime.datetime.now().strftime("%b. %d, %Y")
    h_publish_date = "<h4>{}</h4>\n".format(publish_date)
    h_title = "<h1>{}</h1>\n".format(title)
    subprocess.call(["vim", "posts/.drafts/" + filename])

    return filename, h_title, h_publish_date


def clean_filename(title: str):
    fname = re.sub(r"[^a-z0-9\s]+", "", title.lower())
    fname = re.sub(r"\s+", "-", fname) + ".html"
    return fname

def check_file_exists(filename: str) -> bool:
    with open("posts/postlist.tsv") as postlist:
        post_reader = csv.reader(postlist, delimiter="\t", quotechar='"')
        for row in post_reader:
            if row[1] == filename:
                postlist.close()
                return True
        postlist.close()
        return False

def add_new_post(title: str, filename: str) -> None:
    if check_file_exists(filename):
        sys.exit("Filename already exists. Please delete entries and try again.")
    else:
        with open("posts/postlist.tsv", "a") as postlist:
            post_writer = csv.writer(postlist, delimiter="\t", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            post_time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
            post_writer.writerow([title, filename, post_time])
            postlist.close()

def generate_index() -> None:
    publish_date = datetime.datetime.now().strftime("%b. %d, %Y")
    header, footer = read_boilerplate()
    with open("index.html", "w") as idx:
        idx.write(header + publish_date)
        idx.write("<ul>\n")
        with open("posts/postlist.tsv") as postlist:
            post_reader = csv.DictReader(postlist, delimiter="\t", quotechar='"')
            for row in post_reader:
                entry = "<li>{}: <a href='posts/{}' target='_blank'>{}</a></li>\n".format(row['published'], row['filename'], row['title'])
                idx.write(entry)
            postlist.close()
        idx.write("</ul>\n")
        idx.write(footer)
        idx.close()

def read_boilerplate() -> (str, str):
    header = open(os.path.join("templates/", "header.html")).read()
    footer = open(os.path.join("templates/", "footer.html")).read()
    return header, footer


def create_post():
    fname, title, date = get_input()
    post = open(os.path.join("posts/.drafts/", fname), "r").read()
    header, footer = read_boilerplate()
    with open(os.path.join("posts/", fname), "w") as f:
        f.write(header + title + date + post + footer)
        f.close()

def main():
    # parse out arguments based on user inputs to perform specific actions
    pass

if __name__ == "__main__":
    create_post()
    generate_index()
