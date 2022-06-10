assets
config
gui
services
actionapps

to run:
py vtChunha.py {service} {option}
ex: py C:/Dev/Projects/vtChunha/vtChunha.py whois noimai.com


to compile and build executable:
the executable is built using pyinstall library: https://pypi.org/project/pyinstaller/
pyinstaller --onefile vtChunha.py
OR  pyinstaller "\Python\config\vtChunha.spec"

running as executable:
vtChunha convert  {folderToSearchForISO} (img, iso, dvd, blueray)


