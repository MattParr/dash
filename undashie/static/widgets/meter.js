function meter_model(data) {
    var self = $.observable($.extend(this,data));

    self.trigger("update", self);
    console.log(this);
    return self;
}


function meter_widget(el, data) {
    var model = new meter_model(data);

    model.on("init", function(item) {
        requestAnimationFrame(function(){
            $(el).html($.render(model.template, model));
            meter = $(el).find('.meter');
            meter.val(model.value);
            console.log(meter);
            meter.attr("data-bgcolor", meter.css("background-color"))
                 .attr("data-fgcolor", meter.css("color"))
                 .knob();
        });
    });

    model.on("update", function(item) {
        console.log("update");
        $(el).html($.render(model.template, model));
    });

    /* return the model, which is the important bit */
    return model;
}
