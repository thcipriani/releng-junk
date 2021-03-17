// https://phabricator.wikimedia.org/maniphest/task/edit/parameters/
// title = title
// request url = custom.error.url
// request id = customer.error.reqid
// stack trace = custom.error.stack
javascript:
var get, title, requestUrl, reqId, stackTrace, url;
get = function(elem) {
    return document.querySelector('tr[data-test-subj="tableDocViewRow-' + elem + '"]').childNodes[1].innerText;
};
title = get('exception.class') + ':' + get('exception.message');
requestUrl = 'https://' + get('server') + '/' + get('url');
reqId = get('reqId');
stackTrace = get('exception.trace');
url = "https://phabricator.wikimedia.org/maniphest/task/edit/form/46";
url += '?title=' + encodeURIComponent(title);
url += '&custom.error.url=' + encodeURIComponent(requestUrl);
url += '&custom.error.reqid=' + encodeURIComponent(reqId);
url += '&custom.error.stack=' + encodeURIComponent(stackTrace);
location.href=url;
