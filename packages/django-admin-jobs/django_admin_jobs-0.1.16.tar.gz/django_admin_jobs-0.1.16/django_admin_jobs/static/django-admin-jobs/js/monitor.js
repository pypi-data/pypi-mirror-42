(function($) {

    /* Wait for window load */
    $(function() {
        // find which columns should be updated with the message
        // ignore one position since the link on each row is rendered as a th element by Django
        var startedColIdx = $('th.column-start_time').index() - 1,
            finishedColIdx = $('th.column-end_time').index() - 1,
            statusColIdx = $('th.column-status').index() - 1,
            detailsColIdx = $('th.column-details').index() - 1;

        $.each($('.upload-job-code:not(.finished)'), function(idx, codeElem) {
            var $codeElem = $(codeElem),
                jobId = $codeElem.data('jobid'),
                $row = $codeElem.closest('tr');

            /* Listen for changes */
            new FirebaseListener({
                resourceUrl: '/uploads/' + jobId + '/',
                callback: function(e) {
                    // get columns
                    var $tds = $row.find('> td');

                    // update
                    $($tds.get(statusColIdx)).text(e.status);
                    $($tds.get(detailsColIdx)).text(e.message);
                    $($tds.get(startedColIdx)).text(e.started || '-');
                    $($tds.get(finishedColIdx)).text(e.finished || '-');
                }
            });
        });
    });

})(django.jQuery);