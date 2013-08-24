#PyDashie

PyDashie is a port of [Dashing](https://github.com/Shopify/dashing>) by [Shopify](http://www.shopify.com/>) to Python 2.7.

![Alt text](/path/to/img.jpg)

##Getting Started

You'll need the following native dependencies:

    nodejs

Install using pip:

    pip install -e git+https://github.com/adscott/pydashie.git#egg=PyDashie

Create your dashboard:

    pydashie new myapp

Change directory to `myapp` and start pydashie

    pydashie start example_app

The `example_app` comes with sample widgets & sample dashboards for you to explore. The file structure is setup as follows:

  * `assets` — Images, fonts, and js/coffeescript libraries.
  * `widgets` — The html/css/coffee for individual widgets.
  * `templates\main.html` - Your basic layout.

See `example_app` and `example_samplers` to see how to hook up data sources to widgets.
