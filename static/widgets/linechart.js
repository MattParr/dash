"use strict";

function linechart_model(data) {
    var self = $.observable($.extend(this,data));

    console.log(this);
    return self;
}


function linechart_widget(el, data) {
    var model = new linechart_model(data);

    model.on("init", function() {
        model.trigger("render");
    });

    model.on("render", function() {
        $(el).html($.render(model.template, model));
        requestAnimationFrame(function(){
            var ctx = $(el).find('.chart')[0].getContext("2d");
            var chart = new Chart(ctx).Line({
                labels: Array(model.history.length+1).join(1).split('').map(function(){return '';}),
                datasets: [{
                    data: model.history,
                    fillColor       : "rgba(220,120,120,0.5)",
                    strokeColor     : "rgba(220,120,120,1)"
                }]
            },{
                scaleOverride: true,
                scaleSteps: 10,
                scaleStepWidth: (Math.max.apply(Math, model.history) - Math.min.apply(Math, model.history))/10,
                scaleStartValue: (Math.min.apply(Math, model.history)),
                scaleShowLabels: true,
                animation      : false,
                pointDot       : true 
            });
        });
    });

    model.on("update", function(ev){
        model.history.push(ev.data);
        if (model.history.length > 10) {
            model.history.shift();
        }
        model.trigger("render");
    });

    model.trigger("init");
    /* return the model, which is the important bit */
    return model;
}
