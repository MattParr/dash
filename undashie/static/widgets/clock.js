function clock_model() {
    var self = $.observable(this);

    self.updateTime = function() {
        var h, m, s, today;
        today = new Date();
        h = today.getHours();
        m = today.getMinutes();
        s = today.getSeconds();
        m = self.formatTime(m);
        s = self.formatTime(s);
        self.date = today.toDateString();
        self.time =  h + ":" + m + ":" + s;
        self.trigger("update", self); 
    };

    self.formatTime = function(i) {
        if (i < 10) {
            return "0" + i;
        } else {
            return i;
        }
    };

    setInterval(self.updateTime, 1000);
    return self;
}

function clock_widget(el, data, template) {
    console.log(el);
    model = new clock_model();

    model.on("update", function(item) {
        $(el).html($.render(template, item));
    });
}
