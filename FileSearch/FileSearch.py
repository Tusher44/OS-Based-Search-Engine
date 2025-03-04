import os
import platform
import subprocess


class FileFinder:
    def __init__(self):
        self.os_name = platform.system()

    def get_search_directories(self):
        """Returns common directories to search based on the OS."""
        if self.os_name == "Windows":
            return [os.path.expanduser("~\\Documents"), os.path.expanduser("~\\Desktop"), "C:\\"]
        elif self.os_name == "Darwin":  # macOS
            return [os.path.expanduser("~/Documents"), os.path.expanduser("~/Desktop"), "/"]
        else:  # Linux
            return [os.path.expanduser("~"), "/"]

    def find_file(self, file_name):
        """Searches for a file with the given name in common directories."""
        search_dirs = self.get_search_directories()
        found_files = []

        for directory in search_dirs:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file_name.lower() in file.lower():
                        found_files.append(os.path.join(root, file))

        return found_files if found_files else None

    def find_file_system_wide(self, file_name):
        """Searches for a file system-wide."""
        if self.os_name == "Windows":
            command = f'where /R C:\\ {file_name}'
        else:
            command = f'find / -name "{file_name}" 2>/dev/null'  # macOS/Linux

        try:
            result = os.popen(command).read().strip()
            return result.split("\n") if result else None
        except Exception as e:
            return f"Error searching for file: {e}"

    def open_file(self, file_path):
        """Opens the file using the default application for its type."""
        try:
            if self.os_name == "Windows":
                os.startfile(file_path)  # Windows
            elif self.os_name == "Darwin":
                subprocess.run(["open", file_path])  # macOS
            else:
                subprocess.run(["xdg-open", file_path])  # Linux
            print(f"Opening file: {file_path}")
        except Exception as e:
            print(f"Error opening file: {e}")


if __name__ == "__main__":
    finder = FileFinder()

    while True:
        file_name = input("Enter the file name to search (or type 'exit' to quit): ").strip()
        if file_name.lower() == "exit":
            print("Exiting program.")
            break

        print("\nSearching in common directories...")
        found_files = finder.find_file(file_name)

        if found_files:
            print("\nFound Files:")
            for index, file in enumerate(found_files):
                print(f"{index + 1}. {file}")

            open_choice = input("\nEnter the number of the file to open (or 'no' to skip): ").strip()
            if open_choice.isdigit():
                selected_index = int(open_choice) - 1
                if 0 <= selected_index < len(found_files):
                    finder.open_file(found_files[selected_index])
                else:
                    print("Invalid selection.")
        else:
            print("File not found.")

            choice = input("\nDo you want to search the entire system? (yes/no): ").strip().lower()
            if choice == "yes":
                print("\nSearching system-wide (this may take time)...")
                found_files = finder.find_file_system_wide(file_name)

                if found_files:
                    print("\nFound Files:")
                    for index, file in enumerate(found_files):
                        print(f"{index + 1}. {file}")

                    open_choice = input("\nEnter the number of the file to open (or 'no' to skip): ").strip()
                    if open_choice.isdigit():
                        selected_index = int(open_choice) - 1
                        if 0 <= selected_index < len(found_files):
                            finder.open_file(found_files[selected_index])
                        else:
                            print("Invalid selection.")
                else:
                    print("File not found system-wide.")
