import os

folder_path = "data/images/item"
a = 0
for file_name in sorted(os.listdir(folder_path)):
    old_file_path = os.path.join(folder_path, file_name)

    if os.path.isfile(old_file_path):
        new_name = f"item({a}).png"
        new_file_path = os.path.join(folder_path, new_name)
    
    os.rename(old_file_path, new_file_path)
    a += 1