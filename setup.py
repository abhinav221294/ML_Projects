# Import required modules
from setuptools import find_packages, setup
from typing import List

# Constant for editable installs, commonly written as "-e ."
HYPEN_E_DOT = "-e ."

# Function to read requirements from a requirements.txt file
def get_requirements(file_path: str) -> List[str]:
    """
    Reads a requirements.txt file and returns a list of dependencies.

    Parameters:
    file_path : str
        Path to the requirements.txt file.

    Returns:
    List[str] : List of package requirements
    """
    
    requirements = []  # Initialize an empty list to store requirements

    # Open the file in read mode
    with open(file=file_path) as file_obj:
         # Read all lines from the file
         requirements = file_obj.readlines()
         
         # Remove newline characters from each requirement
         requirements = [req.replace("\n","") for req in requirements]

         # Remove the editable install reference if present
         if HYPEN_E_DOT in requirements:
              requirements.remove(HYPEN_E_DOT)
    
    # Return the cleaned list of requirements
    return requirements

# Setup function to define the package
setup(
   name="STUDENT DATA ML PROJECT",           # Name of the package/project
   version='0.0.1',                           # Version of the package
   author="Abhinav",                          # Author name
   author_email="abhinavanand221294@gmail.com", # Author email
   packages=find_packages(where="src"),       # Automatically find packages under 'src'
   package_dir={'': 'src'},                   # Specify 'src' as the root directory for packages
   install_requires=get_requirements('requirements.txt')  # List of dependencies from requirements.txt
)
