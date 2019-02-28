import sys
import os
import numpy as np

v_tag_to_photo = {}
h_tag_to_photo = {}
v_photo_to_tags = {}
h_photo_to_tags = {}


def store_tag_to_photo(v_tag_to_photo, h_tag_to_photo, file_path):
    with open(file_path) as fp:
        num_photo = int(fp.readline())
        for i in range(num_photo):
            line = fp.readline()
            line = line[: len(line) - 1].split(" ")
            # print(line)
            if line[0] == "H":
                h_photo_to_tags[i] = set()
                for j in range(2, len(line)):  # read all tags
                    tag = line[j]
                    if tag in h_tag_to_photo:
                        h_tag_to_photo[tag].add(i)
                    else:
                        h_tag_to_photo[tag] = set()
                        h_tag_to_photo[tag].add(i)
                    h_photo_to_tags[i].add(tag)

            else:
                v_photo_to_tags[i] = set()
                for j in range(2, len(line)):  # read all tags
                    tag = line[j]
                    if tag in v_tag_to_photo:
                        v_tag_to_photo[tag].add(i)
                    else:
                        v_tag_to_photo[tag] = set()
                        v_tag_to_photo[tag].add(i)
                    v_photo_to_tags[i].add(tag)


def estimate_average_photo(tag_to_photo, num_photo):
    estimate = 1.5
    total = 0
    for k in tag_to_photo:
        total += len(tag_to_photo[k])
    return (estimate * total) // num_photo


merged_v_photo_to_tags = {}
merged_v_tag_to_photo = {}
merged_photos = {}


def merge_two_v_photos(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags, v_tag_to_photo,
                       p1, p2, index):
    merged_photos[index] = [p1, p2]  # create new photo

    tags1 = v_photo_to_tags[p1]
    tags2 = v_photo_to_tags[p2]

    new_tags = set.union(tags1, tags2)  # merge two tags

    merged_v_photo_to_tags[index] = new_tags  # store tags to photo

    for t in new_tags:  # store photo to tags
        if t not in merged_v_tag_to_photo:
            merged_v_tag_to_photo[t] = set()
        merged_v_tag_to_photo[t].add(index)

    del v_photo_to_tags[p1]  # delete photo 1 from dictionary
    del v_photo_to_tags[p2]  # delete photo 2 from dictionary

    for t1 in tags1:
        v_tag_to_photo[t1].remove(p1)  # delete photo1 from tags

    for t2 in tags2:
        v_tag_to_photo[t2].remove(p2)  # delete photo2 from tags


def merge_v_photos_action(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags, v_tag_to_photo,index):
    estimate = estimate_average_photo(v_tag_to_photo, len(v_photo_to_tags))
    all_tags = list(v_tag_to_photo)
    # tags = np.random.choice(all_tags, estimate, replace=False)
    # error_tolleration = full_length/(75 * len(v_photo_to_tags))
    error_tolleration = 0.35
    # print(error_tolleration)
    # tags1 = tags[:len(tags) // 2]
    # tags2 = tags[len(tags) // 2:]
    # tag_set_1 = [v_tag_to_photo[t] for t in tags1]
    # tag_set_2 = [v_tag_to_photo[t] for t in tags2]
    # photos_1 = set.intersection(*tag_set_1)
    # photos_2 = set.intersection(*tag_set_2)

    # num_photo = len(v_photo_to_tags) + len(h_photo_to_tags)
    # count = 0
    all_photos = list(v_photo_to_tags)
    two_photos = np.random.choice(all_photos, 2, replace=False)
    # for p1 in v_photo_to_tags:
    #     for p2 in v_photo_to_tags:
    p1 = two_photos[0]
    p2 = two_photos[1]
    if p1 != p2:  # p1, p2 should be indices
        tag_union = set.union(v_photo_to_tags[p1], v_photo_to_tags[p2])
        if abs(len(tag_union) - estimate)/estimate < error_tolleration:
            # print("merging")
            merge_two_v_photos(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags,
                               v_tag_to_photo, p1, p2, index)


def merge_v_photos(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags, v_tag_to_photo):
    # length = len(v_photo_to_tags)
    if len(v_photo_to_tags) == 0:
        return
    full_length = (len(v_photo_to_tags) + len(h_photo_to_tags))
    index = full_length
    merge_v_photos_action(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags, v_tag_to_photo, index)
    while 0 < len(v_photo_to_tags):
        index += 1
        print(len(v_photo_to_tags))
        merge_v_photos_action(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags,
                              v_tag_to_photo, index)



def write_merge_all_photos(merged_photos, merged_v_photo_to_tags, h_photo_to_tags,
                     ph_to_tag_file, mer_ph_file):

    write_merged_photos(merged_photos, mer_ph_file)  # write merged_photos

    all_photo_to_tags = merged_v_photo_to_tags.copy()
    all_photo_to_tags.update(h_photo_to_tags)
    write_photo_to_tags(all_photo_to_tags, ph_to_tag_file)  # write all photo to tags


def write_merged_photos(merged_photos, mer_ph_file):
    f = open(mer_ph_file, "w")
    f.write(str(len(merged_photos)) + "\n")
    for p in merged_photos:
        photos = str(merged_photos[p])
        photos = photos[1: len(photos) - 1].replace(",", "")
        line = str(p) + " " + photos + "\n"
        f.write(line)




def write_photo_to_tags(photo_to_tags, file_path):
    f = open(file_path, "w")
    f.write(str(len(photo_to_tags)) + "\n")
    for p in photo_to_tags:
        tags = str(photo_to_tags[p])
        tags = tags[1: len(tags) - 1].replace(",", "")
        line = str(p) + " " + tags + "\n"
        f.write(line)


store_tag_to_photo(v_tag_to_photo, h_tag_to_photo, "./b_lovely_landscapes.txt")

merge_v_photos(merged_photos, merged_v_photo_to_tags, merged_v_tag_to_photo, v_photo_to_tags, v_tag_to_photo)
write_merge_all_photos(merged_photos, merged_v_photo_to_tags, h_photo_to_tags, "b_all_photo_to_tags.txt", "b_merged.txt")
print("merged_photos")
print(merged_photos)
print(merged_v_photo_to_tags)
print(merged_v_tag_to_photo)

tag_num_list = [len(merged_v_photo_to_tags[p]) for p in merged_v_photo_to_tags]
for t in tag_num_list:
    print(t)

print("mean: ", sum(tag_num_list)/len(tag_num_list))
print("std: ", np.std(np.array(tag_num_list)))

# print(estimate_average_photo(h_tag_to_photo, len(h_photo_to_tags)))
