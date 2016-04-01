USER=$USER

# lets add sub1 via the remote repo to main / sub1 in the end not really needed
git -C main submodule add git@github.com:$USER/sub1.git sub1
# the sub1 repo was cloned and the master branch checked out
# commit and push main
git -C main commit -m "Added sub1 via remote" 
git -C main push


# lets now pull main_somewhere_else and see what happens
git -C main_somewhere_else pull
# shows that sub1 has no content
ls main_somewhere_else/sub1
# you need to register the submodule with init (stuff happens in .git)
git -C main_somewhere_else submodule init
# and then update it (i.e. pulling the right commit)
git -C main_somewhere_else submodule update
# can also be combined to ... update --init
# the submodule is still in a detached head state, thus alternatively
git -C main_somewhere_else submodule foreach --recursive git checkout master
# will checkout the master of all submodules (you can also go into sub1 and checkout master)
# now you can work in main_somewhere_else exactly the same as in main
meld main/ main_somewhere_else/ # shows that the folders are identical


# we will now change sub1 and push the new version
echo updated >> sub1/readme.txt
git -C sub1 commit -a -m "updated sub1" 
git -C sub1 push
# main now wants the new version of the submodule 
# --remote gets the newest sub1
# --merge merges these changes in the master branch (instead of creating detached head)
git -C main submodule update --remote --merge
# we commit and push this version change in main (not the sub1 content)
git -C main commit -a -m "updated submodule" 
git -C main push
# lets pull these changes in main_somewhere_else
git -C main_somewhere_else pull
git -C main_somewhere_else submodule update --merge # bc the submodule changed


# now both main and main_somewhere_else change sub1
echo good_idea > main/sub1/idea.txt
git -C main/sub1 add idea.txt
git -C main/sub1 commit -a -m "added idex.txt" 
git -C main commit -a -m "updated submodule"
# with --recurse-submodules=on-demand all submodules that need push will be pushed
git -C main push --recurse-submodules=on-demand
# now main_somewhere_else changes sub1 as well
echo v2 >> main_somewhere_else/sub1/readme.txt
git -C main_somewhere_else/sub1 add idea.txt
git -C main_somewhere_else/sub1 commit -a -m "v2 ideas"
git -C main_somewhere_else commit -a -m "updated submodule"
# before pushing main_somewhere_else needs to pull (bc push fails...)
git -C main_somewhere_else pull
# automatic merging cannot work here
# lets go merge sub1
git -C main_somewhere_else/sub1 pull #merge
# now we get rid of the merge conflict and choose local (since thats the one we merged)
git -C main_somewhere_else mergetool
git -C main_somewhere_else commit -a -m "merged"
git -C main_somewhere_else push --recurse-submodules=on-demand
# and finally update main again
git -C main pull
git -C main submodule update --merge


# we want to copy sub2 into main and declare it a submodule
cp -r sub2 main/sub1
# ./ is important here
git -C main/sub1 submodule add ./sub2
git -C main/sub1/sub2 remote show origin
nano main/sub1/.gitmodules #change the url to the correct one (instead of the file)
git  -C main/sub1/ submodule sync #syncronizes the new url in .git/...

# commit and push
git -C main/sub1 commit -m "Added sub2 via copy"
git -C main commit -a -m "updated subm"
# --recurse-submodules=on-demand is only one level :-/
git -C main submodule foreach --recursive git push
git -C main push
# pull new submodule in main_somewhere_else (we need init everytime a new submod is added)
git -C main_somewhere_else pull
# --init will initialize new submodules
# --recursive allows for subsubmodules
git -C main_somewhere_else submodule update --recursive --init --merge
git -C main_somewhere_else submodule foreach --recursive git checkout master

#if you want to clone a repo with submodules you can use
git clone --recursive git@github.com:$USER/main.git third_main
git -C third_main submodule foreach --recursive git checkout master

# conclusion:
# to use submodules effectivly substitute the following commands

# clone
git clone 'url' 'name'
# to
git clone --recursive 'url' 'name'
cd 'name'
git submodule foreach --recursive git checkout master

# push
git push
# to
git push --recurse-submodules=on-demand
git submodule foreach --recursive git push # this is only needed for subsubmodules

# pull
git pull
# to
git pull
git submodule update --recursive --init --merge
git submodule foreach --recursive git checkout master

# always having the master branch checked out is a matter ot taste, not necessary
