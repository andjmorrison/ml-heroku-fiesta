# ml-heroku-fiesta
Example Heroku app using TF and Flask
* [x] Save model post-training.
* [x] Generate req file and purge unused libraries. 
* [x] Procfile for Heroku app startup.
* [x] Test app locally using .env file.
* [x] Push to GitHub.
* [x] Create new app in Heroku, link to GitHub repo.
* [x] Set config variable(s) in settings.
* [x] Build.

---
FAQ
> My app won't deploy! It will not finish the build.

* Try checking the Heroku logs for an error message pointing you to a particular package or dependency.

> My deployment is too big! Heroku says they only host 500 mb for my app.

* Pare down the packages you're using in your req file. Only configure your app with the packages you need. If you have done that and you are still over the limit, change the package(s) used. The default version of Tensorflow (currently 2.4) defaults to the GPU version, which may contain unneeded functions, etc. In that case, specify the CPU version explicity.