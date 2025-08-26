# Getting Started

To start your new PDCR project, you have to create a folder with the project name, Then within that folder you have to create an `access.json` file.
<br><br>
This is some basic syntax for an access.json
```json
{
  "root":"main.lua",
  "files": {}
}
```
The root object tells the engine which file to start the code in i.e. main.lua
The files object will tell the engine which other lua files to use.
<br><br>
Example files object:
```json
"files" : {
  "A":"a.lua",
  "B":"folder/b.lua" // Used to denote subdirectories
}
```

