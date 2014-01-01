/* Model */
function Dashboard() {
  var self = $.observable(this);

  self.widgets = [];
  self.widget_margins = [5, 5];
  self.widget_base_dimensions = [300, 360];
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

  var templates = {};

  dash = window.dashboard = new Dashboard();

  root = $('.gridster');
  $(document).ready(function(){
    root.width(dash.contentWidth);
    $('.gridster ul').gridster({
      widget_margins: dash.widget_margins,
      widget_base_dimensions: dash.widget_base_dimensions,
      avoid_overlapped_widgets: true
    });
    console.log("Gridster set.");    
  });


  dash.on("add", function(item) {
    if(!(item.kind in templates)) {
      /* Load templates,styles and behavior */
      $('head').append('<link rel="stylesheet" type="text/css" href="widgets/' + item.kind + '.css">');
      $.get('widgets/' + item.kind + '.html', function(data) {
        templates[item.kind] = data;
        $.getScript('widgets/' + item.kind + '.js', function() {
          console.log("Loaded " + item.kind);
          self.trigger("init", item);
        })
      })
    }
  });

}).call(this);
