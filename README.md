# PyDashie

PyDashie is a port of [Dashing](https://github.com/Shopify/dashing>) by
[Shopify](http://www.shopify.com/>) to Python 2.7.

## Getting Started

You'll need the following native dependencies:

    nodejs

### Install using pip:

    pip install -e git+https://github.com/lurst/pydashie.git#egg=PyDashie

### Or, alternatively, create a virtual environment and run pydashie from it:

    git clone https://github.com/lurst/pydashie.git
    cd pydashie
    mkvirtualenv pydashie
    python setup.py

Now you can follow the same instructions with the virtualenv activated

### Create your dashboard:

    pydashie new myapp

### Change directory to `myapp` and start pydashie

    pydashie start myapp

The `example_app` comes with sample widgets & sample dashboards for you to 
explore. The file structure is setup as follows:

  * `assets` — Images, fonts, and js/coffeescript libraries.
  * `widgets` — The html/css/coffee for individual widgets.
  * `templates\main.html` - Your basic layout.

See `example_app` and `example_samplers` to see how to hook up data sources 
to widgets.
