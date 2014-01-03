/* Model */
function Dashboard() {
    var self = $.observable(this);

    self.widgets = [];
    self.widget_margins = [5, 5];
    self.widget_base_dimensions = [220, 240];
    self.numColumns = 4;
    self.contentWidth = (self.widget_base_dimensions[0] + self.widget_margins[0] * 2) * self.numColumns;

    $.get("/widgets/list.json", function(data){
        console.log(data);
        $.each(data.widgets, function(i) {
            self.trigger("add", data.widgets[i]);
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
                    dashboard.trigger("loaded", item);
                    console.log("done");
                })
            })
        }
    });

    dashboard.on("loaded", function(item) {
        var sizex = (item.sizex || 1),
            sizey = (item.sizey || 1),
            el = grid.add_widget('<li>' + templates[item.kind] + '</li>', sizex, sizey);
        el.addClass('widget-' + item.kind);
         /* inject the template and pass it on to the widget */
        widget = window[item.kind + '_widget'](el, $.extend(item, {template: templates[item.kind]}));
        dashboard.widgets.push(widget);
    })

}).call(this);
