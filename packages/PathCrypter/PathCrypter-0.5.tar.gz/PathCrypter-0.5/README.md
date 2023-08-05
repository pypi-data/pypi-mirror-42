# Path Encoder
## Description
This application allows encryting files and folder using AES. The content of a file gets encrypted using AES. The
name of a file or folder gets obfuscated. *Hence be aware that file- and folder-names can be reverse-engineered
with minimal effort.*

The tool is essentially a PYTHON 3 script. When installing the package through PIP, a shell script (OS X and Linux) or
BATCH file (MS Windows) is installed as well. This allows easy use of the tool from command line.

### Installation
The package can be installed directly through PIP:

```
pip install pathcrypter 
```
 
## Usage
The tool comes with a shell script (OS X and Linux) or batch file (MS Windows):
```
pathcrypter [-h] [-p PASSWORD] [-e] [-d] [-n] path
```
 
The script takes the following command line arguments:
* **-e**: Encrypt the file or folder
* **-d**: Decrypt the file or folder
* **-n**: Ignore errors
* **-p**: Password to be used for encryption/decryption. *Do note that providing the password as a command line
argument is insecure. This option is available primarily for scripting/automation use.* If no password is provided
using this argument, the password is asked at runtime. This prevents the password from being displayed (readable).
* **path**: The path to the file or folder to be encrypted/decrypted. When specifying a folder, the entire folder content
gets processed (recursively).
