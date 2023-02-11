# CTF challenge built on top of the git

## Generate the challenge

To generate the challenge, edit the different parameters at the beginning of the python file (`LINE`, `N_LINES`, `TOKEN`, `REMOTE`, `PEOPLE_MAIN`, `PEOPLE_END`).


It will generate a `ctf-base` folder containing only a commit saying the player should set up the remote and the `ctf` folder that should be pushed to the remote. Players shouldn't have write access to the remote.

## Solutions to the challenge

The solution of the challenge goes like this:

1. `git log` will show you to put the remote (as set as in the generation file).
2. `git remote add origin whatever` will add the remote
3. `git fetch` to fetch the information
4. `git branch --set-upstream-to=origin/main main` to set the upstream for the current branch
5. `git pull` to fetch and merge the latest modification
6. `git log` to see that you should look at someone's commit (defined in the configuration file). Let's say it's Josh Baker.
7. `git log --author="Josh Baker"`. Locate previous commit to commit with `Ooops. That was actually a secret` commit message. Let's say id is 197cdd167a73197968bdbb9fc6a5709dc9cbfe07.
8. `git checkout 197cdd167a73197968bdbb9fc6a5709dc9cbfe07` to checkout to this version of the code.
9. `cat secrets.txt` to see the content of the file. It will say to look at some line (defined in the script) of the file `text.txt`. Let's say it's line 33.
10. `git blame -L 33,33` to see the owner of the branch you should see. Let's say it's Fraser Fisher.
11. `git checkout FraserFisher` to switch branch.
12. `git log` it will say to look at the difference between two commits (let's say `73c813e` and `e208c2c`).
13. `git diff 73c813e e208c2c` to find the string.

## Generating the docker image

Don't forger to change the root password in the Dockerfile.

You should put an ssh key for a user with read access to the remote in the `ssh` folder (`id_rsa` and `id_rsa.pub`).

You can generate the image with `docker build . -t <username>/git-ctf`

You can then generate an archive of your image with `docker save -o dockerctf.tar <username>/git-ctf`.

## A possible improvement ot the challenge

The challenge can be finished very fast using the `git grep` command if you know the format of the ctf string.

A possible improvement would be to create decoys in the repo or to not give the format of the ctf string to the players.

## A website for the challenge

You can check https://github.com/nanoy42/git-ctf-website to have a small website to host the challenge.