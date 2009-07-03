
=======
Method1
=======

This method uses the pre-packaged .egg file.

1. Download the file 'swat-deployment-1.tar.gz' in the downloads
area

2. Unpack

3. Execute 
     # ./deploy-swat

chmod +x first. This will create a Python virtual environment
so it won't mess with your current Python stuff.

4. Execute 
     # ./run-swat. 

chmod +x first. If all goes well the server will start in port 5000.

5. Open your browser and go to the address http://localhost:5000

=======
Method2
=======

This method requires you to create the .egg file and pull the git
repository

1. git-pull this repository

2. enter the main dir and run
     # python setup.py bdist_egg

3. Right now the best way is to follow method nº1, starting at step 2 
and replace the .egg file in the unpacked content. After replacing
just continue with the rest of method nº 1
