==============
Git and GitHub
==============

This page will walk you through the best practices for using Git and GitHub for CAM\ :sup:`2`\ .

Basic Git and GitHub
--------------------

Git is version control software. If you are unfamiliar with Git, please read through its `getting started guide`_ and seek basic training before continuing with this guide.

GitHub is a website that hosts Git repositories. You are currently using it right now! If you are unfamiliar with GitHub, please complete `GitHub "Hello World" guide`_ before continuing with this guide.


.. _`Frequently Used Git Commands`:

Frequently Used Git Commands
---------------------------------

======================================= ===============================================================================================
 Command                                Description                                                                                   
======================================= ===============================================================================================
 :code:`git clone <repository_url>`     Clone repository to local disk                                                                
 :code:`git status`                     Show files changes since last commit [1]_                                
 :code:`git add <filename/pattern>`     Add untracked or modified files to staging area [2]_                
 :code:`git commit -m "<commit msg>"`   Commit files from staging area with commit message [2]_             
 :code:`git commit -am "<commit msg>"`  Directly commit all modified files with commit message, skiping staging area                  
 :code:`git branch`                     List local branches                                                                           
 :code:`git branch -a`                  List local and remote branches                                                                
 :code:`git branch -d <branch>`         Delete the local branch named :code:`<branch>`                                                      
 :code:`git checkout <branch>`          Switch to local or remote branch named :code:`<branch>`                                             
 :code:`git checkout -b <branch>`       Create and switch to a new local branch named :code:`<branch>`                                      
 :code:`git fetch`                      Fetch all latest changes info from remote repository, won't change any local file             
 :code:`git push`                       Push your branch to remote repository                                                         
 :code:`git push <remote> <branch>`     First push a new :code:`branch` to remote repository with name :code:`remote`                             
 :code:`git pull`                       Pull your branch to the remote repository                                                     
 :code:`git remote prune origin`        Delete any local branches that were deleted in the remote repository                          
======================================= ===============================================================================================

Managing branches
------------------

Branches are very important when working with Git. If have not used branches with Git before, please read `this page`_ to learn the basics.

There are a few protected branches that are important to CAM\ :sup:`2` front-end developers:

- :code:`master`: contains source code of CAM\ :sup:`2` staging site with most recent functional feature.
- :code:`release`: contains source code of CAM\ :sup:`2` production site, stable version of master branch.
- :code:`gh-pages`: (optional) contains front-end code of github documentation page, automatically built.

No work should be done on these branches. All work must be done on a feature branch, a short-lived branch extended from :code:`master` branch. A feature branch should have a meaningful name indicating feature or fix that this branch will implement. After completion, feature branch is merged back to :code:`master`. In general, only repository managers should merge to protected branches.

Issuing a pull request
----------------------

The Purpose of making pull request is to make other team members and someone who interested in this repository keep track of the progress of a new feature branch. team members and leaders can commit, review, provide advice on this branch and every commit is visiable to everyone. For an overview of pull requests, please see `about pull request`_.

Once making first commit of a new feature branch, A pull request should be set up. To initiate a pull request, go to project GitHub and click "New Pull Request". On the following page, make sure base branch is :code:`master` and compare branch is your new feature branch. If necessary, modify title so that it is a descriptive phrase describing the purpose of the branch you are merging. On this page you can also add a more detailed description. Finally, click "Create Pull Request", and you will be redirected to the pull request page. When your feature branch is ready to be merged, leave a comment so that reviewers know.

Cleaning up
------------

Once your feature branch has been merged, the merging contributor will delete the branch as it is no longer needed. Now you can remove the branch on your local repository. Open a terminal, navigate to your repository, and switch to the :code:`master` branch. delete local branch and tracking information of remote branch with `Frequently Used Git Commands`_.


.. [1] Always check :code:`git status` before add or commit to prevent adding unwanted files. :code:`git add .` is not a good practice
.. [2] For Git commit workflow, see `The Three Stages`_


.. _`getting started guide`: https://git-scm.com/doc
.. _`GitHub "Hello World" guide`: https://guides.github.com/activities/hello-world/
.. _`The Three Stages`: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics#_the_three_states
.. _`this page`: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
.. _`about pull request`: https://help.github.com/articles/about-pull-requests/
