import compare50
from grading_script import grader

from pathlib import Path
import shutil
import os
import glob
import sys
import subprocess


# finds the output directory from grading_script module
def get_extracted_dir():
        
    search_dir = Path(".")
    
    for file_path in search_dir.iterdir():
        if file_path.is_dir() and f"{file_path}".startswith("StudentSubmissions"):
            print("Found submission directory from grader script")
            return file_path
    
    return None
    


# deletes the log files from grading_script output
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

# prepares an individual student directory for the compare50 cli
def prepare_student(student_dir):
    p = Path(student_dir)


    only_dirs = [d for d in p.iterdir() if d.is_dir()]
    if len(only_dirs) <= 1:
        return


    # delete everything except the most recent submission
    newest = max(only_dirs, key=lambda d: d.name)
    for d in only_dirs:
        if d != newest:
            shutil.rmtree(d)

# get the name out the output directory
# if cli flag --name is passed, used that
# otherwise, prompt
def get_output_name():
    if "--name" in sys.argv:
        name_index = sys.argv.index("--name") + 1
        if name_index < len(sys.argv):
            return sys.argv[name_index]
        else:
            print("Error: --name flag provided but no name given")
            sys.exit(1)

    course = input("course: ")
    semester = input("Semester: ")
    project = input("Project #: ")
    
    return f"{course}-{semester}-Project{project}-comparison"

def main():
    
    # todo error check this
    input_file = sys.argv[1]
    print(f"input file: {input_file}")
    grader.extract_all_from_zip(input_file)

    out_dir = get_output_name()
    
    extracted_dir = get_extracted_dir()
    if extracted_dir == None:
        print("Error: could not find extraction directory")
        return
    
    delete_log_files()
    
    temp_dir = "temp"
    os.rename(extracted_dir, temp_dir)
    
    for student_dir in Path(temp_dir).iterdir():
        
        if student_dir.is_dir():
            prepare_student(student_dir)
        
    
    #  there is a real api for this, but its very poorly documented
    subprocess.run(
        ["compare50", "*"],
        cwd=temp_dir,
        check=True,
    )
    
    shutil.move(f"{temp_dir}/results", ".")
    os.rename("results", out_dir)
    
    shutil.rmtree(temp_dir)
    



if __name__ == "__main__":
    main()


