USER=mskoenz

# remove remote repos

curl -s -u $USER https://api.github.com/repos/mskoenz/main -X DELETE
curl -s -u $USER https://api.github.com/repos/mskoenz/sub1 -X DELETE
curl -s -u $USER https://api.github.com/repos/mskoenz/sub2 -X DELETE

# remove local repo

rm -rf main
rm -rf main_somewhere_else
rm -rf third_main
rm -rf sub1
rm -rf sub2
