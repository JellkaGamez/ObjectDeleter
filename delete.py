import gzip, base64, random

# ask for .gmd file
file = input("Enter .gmd file: ")

# open .gmd file
with open(file, "rb") as f:
    gmd = f.read()

# helper functions
def text_after(text, str):
    return text[text.find(str.encode('utf-8')) + len(str.encode('utf-8')):]

def text_before(text, str):
    return text[:text.find(str.encode('utf-8'))]

# more complex helper functions
def remove(text, strs: list, ba: str):
    for i in range(len(strs)):
        if ba[i] == 'a':
            text = text_after(text, strs[i])
        elif ba[i] == 'b':
            text = text_before(text, strs[i])
    return text

# decode .gmd file
name = remove(gmd, ['<s>', '<s>', '</s>'], 'aab')
lv_code = remove(gmd, ['<s>', '<s>', '<s>', '</s>'], 'aaab')

# save to a temporary file
with open(f"temp/p1/{file}.txt", "w") as f:
    f.write(lv_code.decode('utf-8'))

# decode the lv code
lv_code = base64.urlsafe_b64decode(lv_code)
lv_code = gzip.decompress(lv_code)

# save to a temporary file
with open(f"temp/p2/{file}.txt", "w") as f:
    f.write(lv_code.decode('utf-8'))

# extract the metadata
metadata = text_before(lv_code, ';')

# extract the object data
object_data = text_after(lv_code, ';')

# save to a temporary file
with open(f"temp/p3/{file}.txt", "w") as f:
    f.write(object_data.decode('utf-8'))

# split at every ;
object_data = object_data.decode('utf-8')
object_data = object_data.split(';')

# ask for a percentage
percentage = float(input("Enter percentage: ")) / 100

# save to a temporary file
with open(f"temp/p4/{file}.txt", "w") as f:
    f.write(f'{object_data}')

# print some information
print("Total objects: " + str(len(object_data)))
print("Objects to remove: " + str(int(len(object_data) * percentage)))

# remove a percentage of the objects at random
for i in range(int(len(object_data) * percentage)):
    object_data.pop(random.randint(0, len(object_data) - 1))

# combine the object data with ;
object_data = ";".join(object_data)

# save to a temporary file
with open(f"temp/p5/{file}.txt", "w") as f:
    f.write(f'{object_data}')

# add metadata
final_lv = metadata.decode('utf-8') + object_data

# save to a temporary file
with open(f"temp/p6/{file}.txt", "w") as f:
    f.write(f'{final_lv}')

# encode the lv code
final_lv = gzip.compress(final_lv.encode('utf-8'))
final_lv = base64.urlsafe_b64encode(final_lv)

# insert the final_lv data into the original .gmd file
with open(file, 'r') as f:
    data = f.read().encode('utf-8')

# get the header
first_s_tag = data.find(b'<s>')
second_s_tag = data.find(b'<s>', first_s_tag + 1)
third_s_tag = data.find(b'<s>', second_s_tag + 1)
header = data[:third_s_tag]
header.replace(name.decode('utf-8'), f'{name.decode('utf-8')} broken')

# get the footer
footer = remove(data, ['<s>', '<s>', '<s>', '</s>'], 'aaaa')

# combine the header, final_lv and footer
final = header + final_lv + footer

# save to a final file
with open(f"{name.decode('utf-8')}R.gmd", 'wb') as f:
    f.write(final)