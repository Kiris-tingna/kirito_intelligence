let util = {

};
util.title = function (title) {
    title = title ? title + ' - SNIP' : 'Kirito Deep Learning Intelgence Platform';
    window.document.title = title;
};

export default util;