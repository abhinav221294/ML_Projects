# Import setup and find_packages from setuptools
# setup() is used to define project metadata and configuration
# find_packages() automatically finds all packages (folders containing __init__.py)
from setuptools import find_packages, setup

# Import List for type hinting (helps with readability and clarity)
from typing import List


# This constant represents "-e ."
# In requirements.txt, "-e ." means:
# "Install the current project in editable mode"
# We will remove it because it should not be treated as a normal dependency
HYPEN_E_DOT = "-e ."


# Function to read and clean requirements.txt file
def get_requirements(file_path: str) -> List[str]:
    """
    This function reads the requirements.txt file
    and returns a clean list of dependencies.
    
    Parameters:
    file_path (str): Path to requirements.txt
    
    Returns:
    List[str]: List of dependency strings
    """

    # Initialize empty list to store requirements
    requirements = []
    
    # Open the requirements.txt file
    # file=file_path → specifies which file to open
    # as file_obj → creates a file object to read content
    with open(file=file_path) as file_obj:
        
        # Read all lines from file
        # Example:
        # ["numpy\n", "pandas\n", "-e .\n"]
        requirements = file_obj.readlines()
        
        # Remove newline characters "\n" from each line
        # So "numpy\n" becomes "numpy"
        requirements = [req.replace("\n", "") for req in requirements]
        
        # If "-e ." exists in requirements list,
        # remove it because it is not an actual library dependency
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    # Return cleaned list of dependencies
    return requirements


# setup() function defines metadata and configuration of the project
setup(
    
    # Name of your project (used when installing package)
    name="clv-ml-project",
    
    # Version number of your project
    # Follow semantic versioning: major.minor.patch
    version="0.0.1",
    
    # Author name
    author="Abhinav",
    
    # Author email (currently empty)
    author_email="abhinavanand221294@gmail.com",
    
    # Automatically find all packages inside the "src" folder
    # A package = folder containing __init__.py
    packages=find_packages(where="src"),
    
    # This tells Python that the root package directory is "src"
    # Meaning: all packages are inside src folder
    package_dir={'': 'src'},
    
    # Install required dependencies from requirements.txt
    # This calls the get_requirements() function
    install_requires=get_requirements('requirements.txt')
)