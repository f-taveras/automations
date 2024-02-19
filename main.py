import os
import shutil
from rich.console import Console
from rich.prompt import Prompt

console = Console()


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        console.print(f"Folder '{folder_name} created.", style="green")
    else:
        console.print(f"Folder '{folder_name} already exists.", style="yellow")

def move_documents_for_deleted_user(user_folder, temp_folder):
    create_folder(temp_folder)
    if os.path.exists(user_folder):
        for filename in os.listdir(user_folder):
            shutil.move(os.path.join(user_folder, filename), temp_folder)
        console.print(f"Documents moved to '{temp_folder}'.", style="green")
    else:
        console.print("User folder does not exists", style="green")
        
def sort_documents(folder):
    log_folder = os.path.join(folder, "logs")
    mail_folder = os.path.join(folder, "mail")

    create_folder(log_folder)
    create_folder(mail_folder)


    for filename in os.listdir(folder):
        if filename.endswith(".log"):
            shutil.move(os.path.join(folder, filename), mail_folder)

    console.print("Documents sorted.", style="green")


def parse_log_file(log_folder):
    error_file_path = os.path.join(log_folder, "errors.log")
    warning_file_path = os.path.join(log_folder, "warnings.log")

    for filename in os.listdir(log_folder):
        if filename.endswith(".log"):
            with open(os.path.join(log_folder, filename), 'r') as file:
                with open(error_file_path, 'w') as error_file, open(warning_file_path, 'w') as warning_file:
                 for line in file:
                     if "ERROR" in line:
                         error_file.write(line)
                     elif "WARNING" in line:
                         warning_file.write(line)

    console.print("Log file parsed for errors and warnings", style="green")
                    
def backup_folder(source_folder, backup_folder):
    create_folder(backup_folder)
    for filename in os.listdir(source_folder):
        shutil.copy(os.path.join(source_folder, filename), backup_folder)
    console.print(f"Backup of '{source_folder}' completed", style="green")

def main():
    while True:
        console.print("Automation Tasks", style="bold underline")
        tasks = {
            "1": ("Create a new folder", create_folder, "Enter folder name: "),
            "2": ("Handle a deleted user", move_documents_for_deleted_user, "Enter user folder, and a temporary folder path: "),
            "3": ("Sort documents into folders", sort_documents, "Enter folder to sort: "),
            "4": ("Parse log file for errors and warnings", parse_log_file, "Enter log folder: "),
            "5": ("Backup specific folders", backup_folder, "Enter source folder, Backup folder: "),    
            "exit": ("Exit the application", None, None) 
        }

        for key, value in tasks.items():
            if key != "exit":
                console.print(f"{key}. {value[0]}")
        console.print("Type 'exit' to quit the application")

        choice = Prompt.ask("Choose a task to execute", choices=tasks.keys())


        if choice == "exit":
            console.print("Existing application. Goodbye!", style="bold red")
            break


        if choice in tasks and tasks[choice][1] is not None:
            task = tasks[choice]
            if ',' in task[2]:
                args = Prompt.ask(task[2]).split(',')
                task[1](*[arg.strip() for arg in args])
            else:
                arg = Prompt.ask(task[2])
                task[1](arg)
        else:
            console.print("Invalid choice.", style="red")

if __name__ == "__main__":
    main()