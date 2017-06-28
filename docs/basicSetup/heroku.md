# [Guide] Heroku
Joseph Sweeney edited this page on Mar 31

___

This page will walk you through some project-specific tasks you might want to perform when using Heroku.

## Table of Contents

+ [Using the Staging Site](#using-the-staging-site)

## Using the Staging Site

It can be difficult to know if the changes you made will compile properly on Heroku. Furthermore, it can be nice to see your changes in action before deploying them. To help with this we will be using a staging site separate from the main Heroku site.

To test the contents of `feature-branch` on the staging site, use

```
git push staging feature-branch:master
```

Then [open the staging site](https://cam2webui-staging.herokuapp.com) and take a look.

To push the master branch to the main Heroku site after having push to the staging site, use

```
git push heroku -f master:master
```