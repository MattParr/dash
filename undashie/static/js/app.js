/* Model */
function Dashboard() {
  var self = $.observable(this);

  self.widgets = [];
  self.widget_margins = [5, 5];
  self.widget_base_dimensions = [220, 220];
  self.numColumns = 4;
  self.contentWidth = (self.widget_base_dimensions[0] + self.widget_margins[0] * 2) * self.numColumns;

  $.get("/widgets/list.json", function(data){
    console.log(data);
    $.each(data.widgets, function(i) {
      item = data.widgets[i];
      self.widgets.push(item);
      self.trigger("add", item);
    })
    console.log(self.widgets);
  });
};


/* Presenter */
(function() {

  console.log("Started.");

  var templates = {}, grid;

  dashboard = new Dashboard();

  $(document).ready(function(){
    $('.gridster').width(dashboard.contentWidth);
    grid = $('.gridster > ul').gridster({
      widget_margins: dashboard.widget_margins,
      widget_base_dimensions: dashboard.widget_base_dimensions
    }).data('gridster');
    console.log("Gridster set.");    
  });

  dashboard.on("add", function(item) {
    if(!(item.kind in templates)) {
      /* Load templates,styles and behavior */
      $('head').append('<link rel="stylesheet" type="text/css" href="widgets/' + item.kind + '.css">');
      $.get('widgets/' + item.kind + '.html', function(data) {
        templates[item.kind] = data;
        console.log("Going for script");
        $.getScript('widgets/' + item.kind + '.js', function() {
          console.log("Loaded " + item.kind);
          dashboard.trigger("loaded", item);
        })
      })
    }
  });

  dashboard.on("loaded", function(item) {
    el = grid.add_widget('<li>' + templates[item.kind] + '</li>', item.sizex, item.sizey);
    el.addClass('widget-' + item.kind);
    widget = window[item.kind + '_widget'](el, item, templates[item.kind]);
    widget.trigger("init");
    console.log(widget);
  })

}).call(this);
