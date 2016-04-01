USER=mskoenz

#Create the following repositories on your git host:

curl -s -u $USER https://api.github.com/user/repos -d '{"name":"main","description":""}'
curl -s -u $USER https://api.github.com/user/repos -d '{"name":"sub1","description":""}'
curl -s -u $USER https://api.github.com/user/repos -d '{"name":"sub2","description":""}'

#If you use github, the following repos should now be done:
#Clone all repos to the folder this file is in.

git clone git@github.com:$USER/main.git
git clone git@github.com:$USER/sub1.git
git clone git@github.com:$USER/sub2.git

#Create some content for all and commit:

echo main > main/readme.txt
echo sub1 > sub1/readme.txt
echo sub2 > sub2/readme.txt

#-C just specifies the path the git command is executed in.

git -C main add readme.txt 
git -C sub1 add readme.txt 
git -C sub2 add readme.txt 

git -C main commit -m "First Commit" 
git -C sub1 commit -m "First Commit"
git -C sub2 commit -m "First Commit"

#Push all changes for the first time

git -C main push -u origin master
git -C sub1 push -u origin master
git -C sub2 push -u origin master

# lets clone main again into main_somewhere_else
git clone git@github.com:$USER/main.git main_somewhere_else
