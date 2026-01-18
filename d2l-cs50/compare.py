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
    # input_file = sys.argv[1]

    name_index = len(sys.argv)
    if "--name" in sys.argv:
        name_index = sys.argv.index("--name")
        
    
    input_files = sys.argv[1:name_index]
    
    print(f"input files: {input_files}")

    temp_files = []

    for (i,file) in enumerate(input_files):
        grader.extract_all_from_zip(file)
        
        
        extracted_dir = get_extracted_dir()
        if extracted_dir == None:
            print("Error: could not find extraction directory")
            return
        
        delete_log_files()
        
        temp_dir = f"temp-{i}"
        temp_files.append(temp_dir)
        os.rename(extracted_dir, temp_dir)
        

    
    final_dir = "final_temp"
    os.mkdir(final_dir)
    for temp in temp_files:
        print(f"temp in tempfiles:{temp}")
        for student_file in Path(temp).iterdir():
            print(f"student_file: {student_file}")
            
            # skip random index file
            # print(f"studentfile name: {student_file.name}")
            if "index.html" in student_file.name:
                
                os.remove(student_file)
                continue
            
            shutil.move(student_file, final_dir)
            
            
    for file in temp_files:
        shutil.rmtree(file)


    out_dir = get_output_name()
    
    
    for student_dir in Path(final_dir).iterdir():
        
        if student_dir.is_dir():
            prepare_student(student_dir)
        
    
    #  there is a real api for this, but its very poorly documented
    subprocess.run(
        ["compare50", "*"],
        cwd=final_dir,
        check=True,
    )
    
    shutil.move(f"{final_dir}/results", ".")
    os.rename("results", out_dir)
    
    os.rename(final_dir, "submissions")
    shutil.move("submissions", out_dir)
    
    
    print("Ignore the above message")
    print(f"To view the results, open {out_dir}/index.html in a browser")



if __name__ == "__main__":
    main()


