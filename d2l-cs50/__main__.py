import compare50
from grading_script import grader

from pathlib import Path
import shutil
import os
import glob
import sys
import subprocess


def get_extracted_dir():
        
    search_dir = Path(".")
    
    for file_path in search_dir.iterdir():
        if file_path.is_dir() and f"{file_path}".startswith("StudentSubmissions"):
            print("Found submission directory from grader script")
            return file_path
    
    return None
    


def delete_log_files():
    pattern = "*.log"

    files_to_delete = glob.glob(pattern)
    print(files_to_delete)

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")

def prepare_student(student_dir):
    p = Path(student_dir)

    dirs = [d for d in p.iterdir() if d.is_dir()]
    if len(dirs) <= 1:
        return


    # delete everything except the most recent submission
    newest = max(dirs, key=lambda d: d.name)
    for d in dirs:
        if d != newest:
            shutil.rmtree(d)

def main():
    grader.extract_all_from_zip("Project 1 Download Jan 11, 2026 843 AM.zip")

    extracted_dir = get_extracted_dir()
    if extracted_dir == None:
        print("Error: could not find extraction directory")
        return
    
    
    delete_log_files()
    
    out_dir_name = "temp"
    os.rename(extracted_dir, out_dir_name)
    
    for student_dir in Path(out_dir_name).iterdir():
        
        if student_dir.is_dir():
            prepare_student(student_dir)
        
    
    
    subprocess.run(
        ["compare50", "*"],
        cwd=out_dir_name,
        check=True,
    )
    
    shutil.move(f"{out_dir_name}/results", ".")

    # if sys.argv[1]:
        

    course = input("course: ")
    semester = input("Semester: ")
    project = input("Project #: ")
    
    os.rename("results", f"{course}-{semester}-{project}-comparison")
    
    
    shutil.rmtree(out_dir_name)
    
    



if __name__ == "__main__":
    main()

