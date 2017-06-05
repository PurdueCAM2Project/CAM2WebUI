This page will walk you through the best practices for using Git and GitHub for CAM<sup>2</sup> front-end development.

## Table of Contents

+ [Basic Git and GitHub](#basic-git-and-github)
+ [Cloning the repository](#cloning-the-repository)
+ [Managing branches](#managing-branches)
    + [Branch management](#branch-management)
    + [Creating a feature branch](#creating-a-feature-branch)
+ [Issuing a pull request](#issuing-a-pull-request)
     + [Pull request best practices](#pull-request-best-practices)
+ [Cleaning up](#cleaning-up)

## Basic Git and GitHub

Git is version control software. If you are unfamiliar with Git, please read through [its getting started guide](https://git-scm.com/doc) and seek basic training before continuing with this guide.

GitHub is a website that hosts Git repositories. You are currently using it right now! If you are unfamiliar with GitHub, please complete [the GitHub "Hello World" guide](https://guides.github.com/activities/hello-world/) before continuing with this guide.

## Cloning the repository

To clone the CAM<sup>2</sup> website repository, copy the link from the main project page. Then, open a terminal, navigate to the directory where you want the cloned repository to appear, and enter
```
git clone <repository_url>
```
where `<repository_url>` is the link you copied. You may use either the HTTPS or SSH link. Please see [this page](https://help.github.com/articles/which-remote-url-should-i-use/) to determine which type is best for you.

## Managing branches

Branches are very important when working with Git. If have not used branches with Git before, please read [this page](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) to learn the basics.

There are a few branches that are important to CAM<sup>2</sup> front-end developers:

- `master`: contains the code that loads when users navigate to the CAM<sup>2</sup> website.
- `development`: contains features that we have not yet released; should be functional.

No work should be done on these branches. All work must be done on a feature branch, a short-lived branch that you create and is quickly merged into the `development` branch.

In general, only the team leaders should merge branches. CAM<sup>2</sup> does not have GitHub permissions set up to enforce this - we expect contributors to be informed and respect the rules. Speak with your team leader if you need clarification.

### Branch management

This section contains some commands that may be useful when managing branches.

| Command                    | Description                                                          |
|:-------------------------- |:-------------------------------------------------------------------- |
| `git branch`               | List local branches                                                  |
| `git branch -a`            | List local and remote branches                                       |
| `git branch -D <branch>`   | Delete the local branch named `<branch>`                             |
| `git checkout <branch>`    | Switch to local or remote branch named `<branch>`                    |
| `git checkout -b <branch>` | Create and switch to a new local branch named `<branch>`             |
| `git push`                 | Push your branch to the remote repository                            |
| `git remote prune origin`  | Delete any local branches that were deleted in the remote repository |

### Creating a feature branch

Before creating a feature branch, come up with a good name for it. The branch name should be short, only a word or two, and indicate the feature or fix that the branch will implement. It should be typed in all lowercase letters and words should be separated by hyphens. Do not use your name as the branch name.

**Examples:** Some good branch names would be `cleanup` or `html-fix`. Some bad branches names would be `CleanUpComments` (too long, capital letters, not separated with hyphens), `jsmith` (includes a name), or `feature` (not descriptive).

Once you have a good name, make sure you are on the `development` branch and have run `git pull` to get any new changes. Create the feature branch with
```
git checkout -b <branch>
```
, where `<branch>` is the name of your feature branch. While working on the feature, make sure you stay on this branch.

To push your feature branch to the remote repository, use
```
git push --set-upstream origin <branch>
```
, where `<branch>` is the name of your feature branch. You only need to use this command the first time your push a new branch; subsequent pushes can be issued with `git push`. After pushing your feature branch, your work is visible for others in the project to view.

## Issuing a pull request

Now that you have finished writing your feature branch, it is ready to be merged back into the `development` branch so that others can begin to use it. To accomplish this, the front-end team uses GitHub pull requests in place of Git merges. These actions are very similar, but GitHub pull requests offer the ability to review code easily before it is accepted. For an overview of pull requests, please see [this page](https://help.github.com/articles/about-pull-requests/).

To initiate a pull request, go the project GitHub and switch to your feature branch. Then click "New Pull Request". On the following page, make sure the base branch is `development`, and NOT `master`. If necessary, modify the title so that it is a descriptive phrase describing the purpose of the branch you are merging. On this page you can also add a more detailed description. Finally, click "Create Pull Request", and you will be redirected to the pull request page.

### Pull request best practices

When working with pull requests, there are a few things you should keep in mind.

- Do not accept your own pull request. Always allow another contributor to accept your pull request only after carefully reviewing your code.
- Submit pull requests early in your feature branch's life, after the first commit if possible. This allows other contributors to comment on your code as you write it.
- Add check boxes to your pull request description. You can use these to indicate tasks that you have and have not completed. To add a checkbox, use the markdown `- [ ] ` for an empty checkbox or `- [x] ` for a filled checkbox.
- When your feature branch is ready to be merged, leave a comment so that reviewers know.

## Cleaning up

Once your feature branch has been merged, the merging contributor will delete the branch as it is no longer needed. Now you can remove the branch on your local repository. Open a terminal, navigate to your repository, and switch to the `development` branch. Now use
```
git branch -D <branch>
```
, where `<branch>` is the name of your merged feature branch, to delete the local branch. Then use
```
git remote prune origin
```
to remove the remote tracking branch. Now you are ready to create another feature branch.