from setuptools import setup, find_packages

def get_dependencies():
    try:
        with open("requirements.txt","r") as rqfile:
            iContent=rqfile.readlines()
        rqfile.close()
        return iContent
    except Exception as e:
        print("Error getting requirements from requirements file")
        print("Error: ",e)
        return []

setup(
    name="pyutils"
    ,version="0.1"
    ,packages=find_packages()
    ,install_requires=get_dependencies()
    ,author="Joan Frago"
    ,description="A python module with lots of useful functions and classes"
)