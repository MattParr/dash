(function() {

  console.log("Yeah! The dashboard has started!");

  Dashboard.on('ready', function() {
    var contentWidth;
    Dashboard.widget_margins || (Dashboard.widget_margins = [5, 5]);
    Dashboard.widget_base_dimensions || (Dashboard.widget_base_dimensions = [300, 360]);
    Dashboard.numColumns || (Dashboard.numColumns = 4);
    contentWidth = (Dashboard.widget_base_dimensions[0] + Dashboard.widget_margins[0] * 2) * Dashboard.numColumns;
    return Batman.setImmediate(function() {
      $('.gridster').width(contentWidth);
      return $('.gridster ul:first').gridster({
        widget_margins: Dashboard.widget_margins,
        widget_base_dimensions: Dashboard.widget_base_dimensions,
        avoid_overlapped_widgets: !Dashboard.customGridsterLayout,
        draggable: {
          stop: Dashboard.showGridsterInstructions
        }
      });
    });
  });

}).call(this);
