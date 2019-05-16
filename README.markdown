# Hyde Reimplementation of the CAM2 Website

This site reimplementation was made to reduce overhead and work times of future members of CAM2 who would need to update content on the site. This site uses the same templates as the original website made in the Summer of 2018, currently using all HTML. There are however some differences between this site and the old site in terms of maintanence.

Because there is no server-side code in Hyde, all of the computation must be done within the template files inside of the "content" folder. The template language ([Jinja2](http://jinja.pocoo.org/docs/2.10/)) is more restrictive than Django, but is easy to understand and learn. All of the templates are located in "content" in the exact location that they will show up for the user. For example, the page "https://cam2project.net/team/" will show up in the file "content/team/index.html". This will make it easy when trying to find which files to modify in order to change content on the site.

Most of the data, however, is not hardcoded into the templates, but is instead stored in the folder called "data". Each file in this folder stores the data for a specific list used by the templates. The names of the fields in each of these lists were taken from the original Django website and may have unintuitive names. Each of the files in this folder has a header at the top that describes what the list does and what each field means.

In order for this site to be run on your computer, Python 2.7 must be installed on your computer and Hyde must be PIP-installed on top of that. Unfortunately, Hyde does not yet work for Python 3, so this is the only way for the site to be run. After installing Hyde, you can launch the webserver to display the content by running the "runSite.py" file in the repository. This will display the site to the user. The site will be displayed on "http://localhost:8080" and can be hard-reloaded by adding "?refresh" to the end of any url on the site.

Things to do:
- Rename unintuitively named fields in the "data" folder
- Convert commonly used pieces of the site to Markdown
- Make publishing script to GitHub Pages using Travis
