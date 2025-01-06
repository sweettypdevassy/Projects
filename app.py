import subprocess
import os

REPO_PATH = "/Users/harisankars/eclipse/exemption4/Projects"  # Path to your GitHub repository
EXEMPTION_BRANCH = "exemption1"  # The branch for exemption

def checkout_exemption_branch():
    """Ensure we are working on the exemption branch."""
    try:
        subprocess.run(f"git checkout {EXEMPTION_BRANCH}", shell=True, check=True)
        print(f"Checked out to branch: {EXEMPTION_BRANCH}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out to branch {EXEMPTION_BRANCH}: {e}")
        raise

def find_class_file(class_name):
    """Find the class file based on the class name."""
    for root, dirs, files in os.walk(REPO_PATH):
        for file in files:
            if file.endswith(".java") and class_name in file:
                return os.path.join(root, file)
    raise FileNotFoundError(f"Class file for {class_name} not found.")

def modify_code_in_repo(class_name, method_name):
    """Modify the code in the Git repository by commenting out the method."""
    try:
        os.chdir(REPO_PATH)
        class_file_path = find_class_file(class_name)

        with open(class_file_path, 'r') as file:
            lines = file.readlines()

        with open(class_file_path, 'w') as file:
            for line in lines:
                if f"public void {method_name}()" in line:
                    line = f"// {line}"  # Comment out the method
                file.write(line)

        print(f"Modified code: Exempting {method_name} in {class_name}.")
        return class_file_path  # Return the modified file path
    except Exception as e:
        print(f"Error modifying the code: {e}")
        return None

def commit_and_push_changes(defect_id, modified_file):
    """Commit changes and push them to the exemption branch."""
    try:
        # Stage the specific modified file
        subprocess.run(f"git add {modified_file}", shell=True, check=True)
        commit_message = f"Exemption for defect {defect_id}"
        subprocess.run(f'git commit -m "{commit_message}"', shell=True, check=True)  # Commit changes
        subprocess.run(f"git push origin {EXEMPTION_BRANCH}", shell=True, check=True)  # Push to the exemption branch

        pr_command = f"gh pr create --title 'Exemption for defect {defect_id}' --body 'Applied exemption changes' --base main --head {EXEMPTION_BRANCH}"
        subprocess.run(pr_command, shell=True, check=True)  # Create pull request

        print(f"PR created for defect {defect_id} from {EXEMPTION_BRANCH} to main.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")

# Example usage
def main():
    defect_id = "DEF-1234"
    class_name = "MyClass"
    method_name = "myMethod"

    # Ensure we are on the correct exemption branch
    checkout_exemption_branch()
    
    # Modify the code in the repo
    modified_file = modify_code_in_repo(class_name, method_name)

    if modified_file:
        # Commit and push changes to the exemption branch
        commit_and_push_changes(defect_id, modified_file)
    else:
        print("No modifications were made.")

if __name__ == "__main__":
    main()

