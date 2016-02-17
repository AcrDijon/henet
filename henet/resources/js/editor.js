var activeXhr = null;
var lastContent = null;

function genPreview() {
    var self = $('textarea#body');
    var rstContent = self.val();
    if (activeXhr || lastContent == rstContent) {
        //activeXhr.abort();
        return;
    }
    lastContent = rstContent;
    activeXhr = $.getJSON({
        'url': '/preview',
        'data': {'rst': rstContent},
        'type': 'POST',
        'error': function(xhr) {
            setPreviewHtml(xhr.responseText);
        },
        'success': function(data) {
            if (data.valid) {
              $('#save').removeAttr('disabled');
            }
            else {
              $('#save').attr('disabled', 'disabled');
            }
            setPreviewHtml(data.result);
            syncScrollPosition();
            activeXhr = null;
        }
    });
}

function syncScrollPosition() {
    var $ed = $('textarea#body');
    var $prev = $('#preview');

    var editorScrollRange = ($ed[0].scrollHeight - $ed.innerHeight());
    var previewScrollRange = (getScrollHeight($prev.contents()) - $prev.innerHeight());

    // Find how far along the editor is (0 means it is scrolled to the top, 1
    // means it is at the bottom).
    var scrollFactor = $ed.scrollTop() / editorScrollRange;

    // Set the scroll position of the preview pane to match.  jQuery will
    // gracefully handle out-of-bounds values.
    $prev.contents().scrollTop(scrollFactor * previewScrollRange);
}

function setPreviewHtml(html) {
    var iframe = $('#preview')[0];
    var doc = iframe.document;

    if (iframe.contentDocument) {
        doc = iframe.contentDocument; // For NS6
    } else if (iframe.contentWindow) {
        doc = iframe.contentWindow.document; // For IE5.5 and IE6
    }
    doc.open();
    doc.writeln(html);
    doc.close();
}



function getScrollHeight($prevFrame) {
    // Different browsers attach the scrollHeight of a document to different
    // elements, so handle that here.
    if ($prevFrame[0].scrollHeight !== undefined) {
        return $prevFrame[0].scrollHeight;
    } else if ($prevFrame.find('html')[0].scrollHeight !== undefined &&
               $prevFrame.find('html')[0].scrollHeight !== 0) {
        return $prevFrame.find('html')[0].scrollHeight;
    } else {
        return $prevFrame.find('body')[0].scrollHeight;
    }
}

