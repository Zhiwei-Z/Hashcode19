import numpy as np

photo_to_tags = {}
merged_photos = {}


def read_merged_photos(file, merged_photos):
    with open(file) as fp:
        num_photo = int(fp.readline())
        for i in range(num_photo):
            line = fp.readline().split(" ")
            m = int(line[0])
            p1 = int(line[1])
            p2 = int(line[2][:len(line[2]) - 1])
            merged_photos[m] = [p1, p2]


def read_all_photos(file, photo_to_tags):
    with open(file) as fp:
        num_photo = int(fp.readline())
        for i in range(num_photo):
            line = fp.readline()
            line = line[: len(line) - 1].split(" ")
            # print(line)
            # if line[0] == "H":
            photo = line[0]
            photo_to_tags[photo] = set()
            for j in range(1, len(line)):  # read all tags
                tag = line[j]
                photo_to_tags[photo].add(tag)


def combine_slide(photo_to_tags, score_file):
    score = 0
    photos = list(photo_to_tags)
    slides = [photos[0]]
    added = set()
    added.add(photos[0])
    photo_array = np.array(photos)
    while len(slides) < len(photos):
        print(len(slides))
        last_photo = slides[len(slides) - 1]
        if len(photos) - len(slides) == 1:
            p1 = np.random.choice(photo_array, 1)[0]
            while p1 in added:
                p1 = np.random.choice(photo_array, 1)[0]
            slides.append(p1)
            score += compute_interest(photo_to_tags, last_photo, p1)
            write_score(score, score_file)
            return slides

        p1 = np.random.choice(photo_array, 1)[0]
        while p1 in added:
            p1 = np.random.choice(photo_array, 1)[0]

        p2 = np.random.choice(photo_array, 1)[0]
        while (p2 in added) or (p1 == p2):
            p2 = np.random.choice(photo_array, 1)[0]

        i1 = compute_interest(photo_to_tags, last_photo, p1)
        i2 = compute_interest(photo_to_tags, last_photo, p2)

        if max(i1, i2) == 0:
            if np.random.random_sample() > 0.01:
                continue
        if i1 >= i2:
            slides.append(p1)
            added.add(p1)
            score += i1
            print("add ", i1)
        else:
            slides.append(p2)
            added.add(p2)
            score += i2
            print("add ", i2)

    return slides


def write_score(score, file):
    f = open(file, "w")
    f.write(str(score) + "\n")

def write_slides(slides, file):
    f = open(file, "w")
    f.write(str(len(slides)) + "\n")
    for i in range(len(slides)):
        photo = int(slides[i])
        if photo in merged_photos:
            f.write(str(merged_photos[photo][0]) + " " + str(merged_photos[photo][1]) + "\n")
        else:
            f.write(str(photo) + "\n")


def compute_interest(photo_to_tags, p1, p2):
    tags1 = photo_to_tags[p1]
    tags2 = photo_to_tags[p2]
    intersect = len(set.intersection(tags1, tags2))
    return min(len(tags1) - intersect, len(tags2) - intersect, intersect)


read_merged_photos("./a_merged.txt", merged_photos)
read_all_photos("./a_all_photo_to_tags.txt", photo_to_tags)
slide = combine_slide(photo_to_tags, "./a_score.txt")
write_slides(slide, "./a_slide.txt")

# read_all_photos("./b_all_photo_to_tags.txt", photo_to_tags)
