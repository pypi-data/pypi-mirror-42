=====
Usage
=====

To use NotebookToAll in a project::


Make sure your notebook doesn't have magic commands in it if you want to create an executable .py script.::


    from notebooktoall.transform import transform_notebooks

    transform_notebooks(ipynb_file="my_jupyter_notebook.ipynb", export_list=["html", "py"])



Run your code and your .html and .py files should appear in your current working directory.

You can pass a Jupyter notebook url to transform_notebooks().
