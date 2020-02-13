import os
import csv

path = 'Music'
files = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.mp4' in file:
            files.append(os.path.join(r, file))

for f in files:
    found = False
    songs = f.split('/')
    song = songs[2].replace('.mp4', '')
    folder = songs[0] + '/' + songs[1]

    with open('Music/metadata_2000.csv') as a, open('Music/metadata-4.csv', 'a') as g:

        reader = csv.reader(a)
        writer = csv.writer(g)

        for row in reader:
            if row[3] == song and row[2] == folder:
                found = True
                writer.writerow(row)
                break

        if not found:
            print(f)
