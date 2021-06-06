import os
import datetime
import re
import subprocess
import csv
import sys
import sqlite3
from contextlib import closing


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
    with closing(sqlite3.connect("blog.db", isolation_level=None)) as connection:
        with closing(connection.cursor()) as cursor:
            matches = cursor.execute(
                "SELECT path FROM posts WHERE path = ?",
                (filename,),
            ).fetchall()
            return len(matches) > 0


def add_new_post(title: str, filename: str) -> None:
    if check_file_exists(filename):
        sys.exit("Filename already exists. Please delete entries and try again.")
    else:
        with closing(sqlite3.connect("blog.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                post_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
                matches = cursor.execute(
                    "INSERT INTO posts VALUES(?, ?, ?, NULL)",
                    (title, filename, post_time),
                )


def generate_index() -> None:
    publish_date = datetime.datetime.now().strftime("%b. %d, %Y")
    header, footer = read_boilerplate()
    with open("index.html", "w") as idx:
        idx.write(header + publish_date)
        idx.write("<ul>\n")
        with closing(sqlite3.connect("blog.db", isolation_level=None)) as connection:
            with closing(connection.cursor()) as cursor:
                posts = cursor.execute(
                    "SELECT * FROM posts ORDER BY published DESC"
                ).fetchall()
        for row in posts:
            entry = "<li>{}: <a href='posts/{}' target='_blank'>{}</a></li>\n".format(
                row[2], row[1], row[0]
            )
            idx.write(entry)
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
