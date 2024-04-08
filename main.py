import os
import shutil
import datetime
from tqdm import tqdm

def main():
    # Prompt the user to select the action
    print("Select action:")
    print("1. Sort files.")
    print("2. Create a list of files in a text file")
    print("3. Compare two folders")
    action_choice = input("Enter the number corresponding to your choice: ")

    # Validate the user's input
    valid_choices = ['1', '2', '3', '4']
    while action_choice not in valid_choices:
        print("Invalid choice. Please enter either 1, 2, 3, 4")
        action_choice = input("Enter the number corresponding to your choice: ")

    # If user selects to sort files
    if action_choice in ['1']:
        # Prompt the user to select the granularity
        print("\nSelect granularity for sorting:")
        print("1. Year")
        print("2. Month")
        print("3. Day")
        print("4. Time")
        selected_granularity = input("Enter the number corresponding to your choice: ")

        # Validate the user's input
        valid_granularity_choices = ['1', '2', '3', '4']
        while selected_granularity not in valid_granularity_choices:
            print("Invalid choice. Please enter a number between 1 and 4.")
            selected_granularity = input("Enter the number corresponding to your choice: ")

        # Map the user's choice to the corresponding time granularity
        granularity_mapping = {
            '1': 'year',
            '2': 'month',
            '3': 'day',
            '4': 'time'
        }
        selected_granularity = granularity_mapping[selected_granularity]

        source_dir = input("Enter the source directory: ")
        destination_dir = input("Enter the destination directory: ")

        # Call function to sort files with the selected granularity
        sort_files(source_dir, destination_dir, selected_granularity)
        print("Files sorted successfully!")

    # If user selects to create a list of files in a text file
    elif action_choice == '2':
        source_dir = input("Enter the source directory: ")
        output_file_path = input("Enter the path for the output text file, make sure to include the file name at the end: ")
        show_path_option = input("Show full file path? (Y/N): ").lower()

        if show_path_option == 'y':
            show_path = True
        else:
            show_path = False
        
        add_comma_option = input("Add comma at the end of each entry? (Y/N): ").lower()

        if add_comma_option == 'y':
            add_comma = True
        else:
            add_comma = False

        # Call function to create a list of files in a text file
        create_file_list(source_dir, output_file_path, show_path, add_comma)
        print("File list created successfully!")
    # If user selects to compare two folders
    elif action_choice == '3':
        folder1 = input("Enter the path of the first folder: ")
        folder2 = input("Enter the path of the second folder: ")
        output_file_path = input("Enter the path for the output text file, make sure to put the file name at the end: ")

    # Call function to compare folders and export differences to a text file
        compare_folders(folder1, folder2, output_file_path)

        print(f"Differences exported to {output_file_path}")
        


    # Add input prompt to prevent terminal from closing immediately
    input("Press Enter to exit...")

def create_file_list(source_dir, output_file_path, show_path=True, add_comma=False):
    # Get a list of all files in the source directory
    files_list = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if show_path:
                file_entry = os.path.join(root, file)
            else:
                file_entry = file
            
            if add_comma:
                file_entry += ','
            
            files_list.append(file_entry)

    # Write the list of files to the output text file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Initialize tqdm progress bar with total number of files
        with tqdm(total=len(files_list), desc="Writing File List", unit="files") as pbar:
            # Write each file path or file name to the output text file
            for file_entry in files_list:
                output_file.write(file_entry + '\n')
                pbar.update(1)  # Increment progress bar


def extract_date_modified(file_path):
    modification_time = os.path.getmtime(file_path)
    modification_datetime = datetime.datetime.fromtimestamp(modification_time)
    return modification_datetime

def extract_date_creation(file_path):
    modification_time = os.path.getctime(file_path)
    modification_datetime = datetime.datetime.fromtimestamp(modification_time)
    return modification_datetime

def sort_files(source_dir, destination_dir, granularity):
    # Initialize a list to store duplicate file paths
    duplicate_files = []

    # Count total number of files
    total_files = sum(len(files) for _, _, files in os.walk(source_dir))

    while True:
        print("1. Sort files on the day that they were created")
        print("2. Sort files on the day that they were modfied")
        MorC = input("What do you want to do")
        if MorC in ['1', '2']:
            break
        else:
            continue

    # Use tqdm to display a progress bar
    with tqdm(total=total_files, desc="Sorting Files", unit="files") as pbar:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)

                if MorC == '1':
                    modification_datetime = extract_date_creation(file_path)

                if MorC == '2':
                    modification_datetime = extract_date_modified(file_path)

                # Extract the relevant time components based on selected granularity
                if granularity == 'year':
                    time_component = modification_datetime.year
                elif granularity == 'month':
                    time_component = modification_datetime.strftime('%Y/%B')
                elif granularity == 'day':
                    time_component = modification_datetime.strftime('%Y/%B/%d')
                elif granularity == 'time':
                    time_component = modification_datetime.strftime('%Y/%B/%d/%H-%M')

                target_directory = os.path.join(destination_dir, time_component)
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)

                # Check if file with the same name exists in the target directory
                dest_file_path = os.path.join(target_directory, file)
                if os.path.exists(dest_file_path):
                    # If file with the same name exists, append a unique identifier
                    filename, ext = os.path.splitext(file)
                    new_filename = filename + "_1" + ext
                    dest_file_path = os.path.join(target_directory, new_filename)

                    # Log the duplicate file path
                    duplicate_files.append((file_path, dest_file_path))

                # Copy the file to the target directory
                shutil.copy(file_path, dest_file_path)
                pbar.update(1)  # Increment progress bar

    # Write the list of duplicates to a log file in the destination directory
    log_file_path = os.path.join(destination_dir, "duplicate_files.log")
    with open(log_file_path, 'w') as log_file:
        for src, dest in duplicate_files:
            log_file.write(f"Duplicate: {src} --> {dest}\n")

def list_files_in_folder(folder):
    """Recursively list all files in a folder."""
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), folder)
            file_list.append(relative_path)
    return file_list

def compare_folders(folder1, folder2, output_file_path):
    """Compare two folders for differences and export to a text file."""
    files_in_folder1 = set([os.path.basename(file) for file in list_files_in_folder(folder1)])
    files_in_folder2 = set([os.path.basename(file) for file in list_files_in_folder(folder2)])

    files_only_in_folder1 = files_in_folder1 - files_in_folder2
    files_only_in_folder2 = files_in_folder2 - files_in_folder1

    with open(output_file_path, 'w') as output_file:
        output_file.write("Files only in folder 1:\n")
        for file in files_only_in_folder1:
            output_file.write(file + '\n')

        output_file.write("\nFiles only in folder 2:\n")
        for file in files_only_in_folder2:
            output_file.write(file + '\n')

    print(f"Differences exported to {output_file_path}")

    print(f"Differences exported to {output_file_path}")

if __name__ == "__main__":
    main()