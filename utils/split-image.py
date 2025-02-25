import os
import shutil
import random

def count_files_in_folder(folder_path):
    # List all the files and directories in the given folder path
    file_list = os.listdir(folder_path)
    # Filter the list to include only files (excluding directories)
    file_list = [f for f in file_list if os.path.isfile(os.path.join(folder_path, f))]
    # Return the number of files in the folder
    return len(file_list)


def split_folder(folder_path, train_ratio=0.2):
    # List all the files in the given folder path
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Shuffle the file list for random distribution
    random.shuffle(file_list)
    
    # Calculate the number of files for training
    train_count = int(len(file_list) * train_ratio)
    
    # Create training and testing directories
    train_folder = os.path.join(folder_path, 'take')
    test_folder = os.path.join(folder_path, 'not_take')
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    
    # Move files to training and testing folders
    for i, file_name in enumerate(file_list):
        src_path = os.path.join(folder_path, file_name)
        if i < train_count:
            dst_path = os.path.join(train_folder, file_name)
        else:
            dst_path = os.path.join(test_folder, file_name)
        shutil.move(src_path, dst_path)

# Example usage
# folder_path = "path/to/your/folder"
# file_count = count_files_in_folder(folder_path)
# print(f"There are {file_count} files in the folder.")

# split_folder(folder_path)
