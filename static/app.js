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

function MangaTitle(name, url, thumbUrl) {
    var self = this;
    self.name = name;
    self.url = url;
    thumbUrlRaw = typeof thumbUrl !== 'undefined' ? thumbUrl : '/static/noThumb.jpg';
    self.thumbUrl = ko.observable(thumbUrlRaw);
    self.chapters = ko.observableArray([]);
    self.tags = ko.observableArray([]);

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

    // ---------------- Using Pytaku REST API: fetch Manga data ------------

    self.init = function() {
        if (self.initStatus() == 0) {
            self.initStatus(1);

            var url = '/api/manga/info?url=' + encodeURIComponent(self.url);
            $.ajax(url, {
                headers: {
                    Pytoken: apiToken,
                    Userid: userId
                },
                success: self.mangaInfoCallback
            });
        }
    }

    self.mangaInfoCallback = function(data, stt, xhr) {
        self.initStatus(2);
        info = JSON.parse(data);

        self.thumbUrl(info['thumbnailUrl']);
        self.tags(info['tags']);

        chapters = info['chapters'];
        for (var i = 0; i < chapters.length; i++) {
            self.chapters.push(new MangaChapter(
                        chapters[i]['title'], chapters[i]['url']));
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
    self = this;

    this.options = {
        showThumbs: true,
        updateMangaList: true,
        updateChapterList: true,
        sites: ['kissmanga']
    };

    this.titles = ko.observableArray([]);
    this.updatingTitles = ko.observable(false);
    this.hasTitles = ko.computed(function() {
        return self.titles().length > 0;
    });

    this.alerts = ko.observableArray([]);

    this.pushAlert = function(msg, type) {
        this.alerts.push(new AlertModel(msg, type));
    };

    this.removeAlert = function(al) {
        this.alerts.remove(al);
    }.bind(this);

    // ---------------------- Init -------------------------
    this.init = function() {

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
    this.init();

    // ------------------ Using Pytaku REST API --------------------------
    this.mangaQuery = ko.observable('');

    this.searchManga = function() {

        self.mangaQuery($.trim(self.mangaQuery()));

        // TODO: Better come up with a solid server-side protection too
        if (self.mangaQuery().length < 2) return;

        self.updatingTitles(true);
        $.ajax('/api/manga', {
            headers: {
                Pytoken: apiToken,
                Userid: userId
            },
            data: {
                keyword: self.mangaQuery()
            },
            success: self.searchMangaCallback,
            complete: function() {
                self.updatingTitles(false);
            }
        });
    }
    this.searchMangaCallback = function(data, textStatus, xhr) {
        ar = JSON.parse(data);
        // Reset title list
        self.titles([]);

        for (var i = 0; i < ar.length ; i++) {
            self.titles.push(new MangaTitle(ar[i]['title'], ar[i]['url']));
        }
    }
}

// Activates knockout.js
var app = new AppViewModel();
ko.applyBindings(app);

// -------------------- Not enough jQuery! ------------------------

// yeah, I great artists steal...
// http://stackoverflow.com/questions/3514784/what-is-the-best-way-to-detect-a-handheld-device-in-jquery
var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

$(document).ready(function() {

    // Enter to fire off search function
    $('#text-search').keypress(function(ev) {
        if (ev.keyCode == 13) {
            $('#btn-search').trigger('click');
        }

    });

    // Put focus on search input field. Mobile users may not want to keyboard
    // to pop up automatically.
    if (!isMobile) {
        $('#text-search').focus();
    }
});

