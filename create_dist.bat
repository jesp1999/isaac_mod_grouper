IF exist dist ( rmdir dist /S /Q )
IF exist build ( rmdir build /S /Q )
pyinstaller isaac_mod_grouper.py
echo "isaac_mod_grouper\isaac_mod_grouper.exe" >> "dist\isaac_mod_grouper.bat"
