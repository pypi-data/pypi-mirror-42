# easycon  
A easy-use tool to connect to a remote server. This tool is developed on `paramiko`. 
## Install  
`pip install easycon` 
## Usage 
The following is the instruction of this tool. One can also find this by run command `easycon` in terminal directly. 

```
{COMMAND}:  
    easycon [options]  
{DESCRIPTION}:   
    An easy tool to control remote (linux-like) server. One must input a <CONFIG>
 file. The <CONFIG> contains all the information, such as IP, port, of the remote  
 server. One can use --template to create a template.   
{OPTIONS}:   
     --config 
        A file contains login info. If you do not have one, consider  '--mkconfig'
        Example: 
                 easycon --config <path> [options]  
        
     --mkconfig
       Create a template login file.  
       Example: 
                 easycon --mkconfig <path> 
        
     --describe 
        Show information of remote server. This can be a test of connection.   
        
     --login  
       Use SSH to connect to the remote server. This makes an interavtive window. 
       Example:  
                 easycon --config <path> --login 
                 
     --dirpath 
       A absolute path of directly (linux form) may be used for many cases. 
        
     --uploadfile 
       upload a file into the remote.  
       Example:  
                 easycon --config <path> --uploadfile <filepath>   [ --dirpath <path> ]
       if a <path> is specified, file will be upload to "/<path>/<filename>"
       if not, file will be put at "/home/<filename>"     
       
     --downloadfile 
       downloadfile a file from the remote.  
       Example:  
                 easycon --config <path> --downloadfile <filepath>  
       <filepath> must be a absolute path such as "/home/ec2-user/file.txt"
       The file will be download the current working directory (CWD)                             
    
```
