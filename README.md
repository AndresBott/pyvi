# Install
## install
clone
run sudo install.py install

this will create a soflink from the cloned dir into the needed dirs


##config
* trust_video_extensions:(Bool) will use the file extension to determine if  file is a video
* only_check_video_extension: (Bool) if set to True and a file does NOT have an extension, it will not be checked for magic mime type

## uninstall
run sudo install.py uninstall


#TODO
* add sub folder and parent folder dynamic playlist

#Changelog
### 04/08/2018
* WIP on data object
* WIP on separation to an mvc model