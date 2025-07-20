#!/bin/bash


echo ">> FETCHING YOUR OWN REPO..."
git clone https://github.com/MKDBGNS/MusicPlayer /MusicPlayer


echo ">> INSTALLING REQUIREMENTS..."
cd /MusicPlayer
pip3 install -U -r requirements.txt

echo ">> STARTING MUSIC PLAYER USERBOT..."
clear
echo "
#     #                        
##   ## #    #  ####  #  ####  
# # # # #    # #      # #    # 
#  #  # #    #  ####  # #      
#     # #    #      # # #      
#     # #    # #    # # #    # 
#     #  ####   ####  #  ####  
                               
######                                    
#     # #        ##   #   # ###### #####  
#     # #       #  #   # #  #      #    # 
######  #      #    #   #   #####  #    # 
#       #      ######   #   #      #####  
#       #      #    #   #   #      #   #  
#       ###### #    #   #   ###### #    # 
                                          
MUSIC PLAYER USERBOT IS SUCCESSFULLY DEPLOYED!
"
python3 main.py
