function MangaChapter(name, url) {
    var self = this;
    self.name = name;
    self.url = url;
    self.selected = ko.observable(false);

    self.toggle = function() {
        if (self.selected()) {
            self.selected(false);
        } else {
            self.selected(true);
        }
    }
}

function MangaTitle(name, thumbUrl) {
    var self = this;
    self.name = name;
    self.thumbUrl = typeof thumbUrl !== 'undefined' ? thumbUrl : '/static/noThumb.jpg';
    self.chapters = ko.observableArray([
        new MangaChapter('Chapter 01 -  Whatever', '#'),
        new MangaChapter('Chapter 02 -  Whatever and here comes a very very very very long title ;)', '#'),
        new MangaChapter('Chapter 03 -  Whatever', '#')
    ]);

    self.canDownloadSelected = ko.computed(function() {
        var ch = self.chapters();
        for (var i = 0; i < ch.length; i++) {
            if(ch[i].selected()) {
                return true;
            }
        }
        return false;
    });

    self.initStatus = ko.observable(0);

    self.init = function() {
        if (self.initStatus() == 0) {
            self.initStatus(1);
            window.setTimeout(function(){
                self.initStatus(2);
            }, 2000);
        }
    }
}

function AlertModel(msg, type) {
    this.message = msg;
    this.type = typeof type !== 'undefined' ? type : 'info';
}

// Shameless stackoverflow ripoff
// http://stackoverflow.com/questions/1403888/get-escaped-url-parameter
function getURLParameter(name) {
    return decodeURI(
            (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
        ).replace(/\+/g, ' ');
}

function AppViewModel() {

    this.options = {
        showThumbs: true,
        updateMangaList: true,
        updateChapterList: true,
        sites: ['kissmanga']
    };

    this.titles = ko.observableArray([
        new MangaTitle('Boo'),
        new MangaTitle('Naruto', 'http://kissmanga.com/Uploads/Etc/8-22-2011/5189522cover.jpg')
    ]);

    this.alerts = ko.observableArray([
        new AlertModel(getURLParameter('msg'), getURLParameter('type'))
    ]);

    this.pushAlert = function(msg, type) {
        this.alerts.push(new AlertModel(msg, type));
    };

    this.removeAlert = function(al) {
        this.alerts.remove(al);
    }.bind(this);
}

// Activates knockout.js
var app = new AppViewModel();
ko.applyBindings(app);
