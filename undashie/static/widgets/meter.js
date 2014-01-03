function meter_model(data) {
    var self = $.observable($.extend(this,data));

    console.log(this);
    return self;
}


function meter_widget(el, data) {
    var model = new meter_model(data);

    model.on("init", function(item) {
        $(el).html($.render(model.template, model));
        meter = $(el).find('.meter');
        meter.attr("data-bgcolor", meter.css("background-color"));
        meter.attr("data-fgcolor", meter.css("color"));
        meter.knob();
    });

    model.on("update", function(item) {
        $(el).html($.render(model.template, model));
    });

    /* return the model, which is the important bit */
    return model;
}
