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
// http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
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

    this.alerts = ko.observableArray([]);

    this.pushAlert = function(msg, type) {
        this.alerts.push(new AlertModel(msg, type));
    };

    this.removeAlert = function(al) {
        this.alerts.remove(al);
    }.bind(this);

    // Alert if there's some message passed in as URL parameters
    var msg = getParameterByName('msg');
    if (msg != '') {
        this.pushAlert(msg, getParameterByName('type'));
    }

    // Is your dropbox account linked? If not, show alert!
    if (!dropboxed) {
        this.pushAlert("You dropbox account has not been linked. Please click 'Authenticate with Dropbox' first.", 'danger');
    }
}

// Activates knockout.js
var app = new AppViewModel();
ko.applyBindings(app);
