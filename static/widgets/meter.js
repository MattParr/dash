"use strict";

function meter_model(data) {
    var self = $.observable($.extend(this,data));

    console.log(this);
    return self;
}


function meter_widget(el, data) {
    var model = new meter_model(data);

    model.on("init", function() {
        requestAnimationFrame(function(){
            $(el).html($.render(model.template, model));
            var meter = $(el).find('.meter');
            meter.val(model.value);
            console.log(meter);
            meter.attr("data-bgcolor", meter.css("background-color"))
                 .attr("data-fgcolor", meter.css("color"))
                 .knob();
        });
    });

    model.on("update", function(item){
        console.log("update");
        $(el).html($.render(model.template, model));
    });

    model.trigger("init");
    /* return the model, which is the important bit */
    return model;
}
