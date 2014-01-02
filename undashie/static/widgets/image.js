function image_model(data) {
    var self = $.observable(this);

    console.log(data);
    self.url = data.url;
    return self;
}


function image_widget(el, data, template) {
    model = new image_model(data);

    model.on("init", function(item) {
        $(el).html($.render(template, model));
    });

    model.on("update", function(item) {
        $(el).html($.render(template, model));
    });

    /* return the model, which is the important bit */
    return model;
}
