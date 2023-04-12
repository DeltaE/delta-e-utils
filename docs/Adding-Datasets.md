# **2. Adding Datasets**

After deciding that a dataset is useful for your research and/or could be useful for other research projects, please open the form to add the datasets by downloading the input.py found in the fornt page of delta-e-utils.

To do this, first you need to create a new branch in delta-e-utils. Then clone the repository on to your machine. Check the README.md on the front page of delta-e-utils on how to do this. Next, you need to install Tkinter and PIL by writing the following into your command line:

Tkinter:
```pip
pip install tk
```

PIL:
```pip
pip install pillow
```
or
```python
python -m pip install --upgrade Pillow
```

After all the above is complete, write the following into yout command line to run the form UI:

```python
python3 input.py
```

Use Page 2 of this how to guide to help with filling the form. After submiting the form it will create a page in: docs/_build/html/index.html which will contain the new dataset you added above, also you will be able to see a python file in src/delta_e/project_name/projectname.py make sure to write all your code and scripting in this .py file.

Once all of this is complete commit and push these changes to your branch by writing:

```git
git add .
```

```git
git commit -m "message"
```

```git
git push
```

A pull request should now be available to you on your github branch. You can review your form and then merge the pull request to the main branch once everything is completed. If there are any conflicts, talk to a member of the data-team to try and get the issue resolved.

Now the dataset is ready to be found in Read the Doc by Delta E+ researchers!

For more complex datasets ensure to write a notebook of how to run the scripts and any additional tips and tricks required to aquire the data from the scripts.