function Dashboard() {
  var self = $.observable(this);

  self.widgets = [];
  self.widget_margins = [5, 5];
  self.widget_base_dimensions = [300, 360];
  self.numColumns = 4;
  self.contentWidth = (self.widget_base_dimensions[0] + self.widget_margins[0] * 2) * self.numColumns;
};

(function() {

  console.log("Started.");

  dash = window.dashboard = new Dashboard();
  $(document).ready(function(){
    $('.gridster').width(dash.contentWidth);
    $('.gridster ul').gridster({
      widget_margins: dash.widget_margins,
      widget_base_dimensions: dash.widget_base_dimensions,
      avoid_overlapped_widgets: true
    });

    console.log("Gridster set.");    
  })


}).call(this);
