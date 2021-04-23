jQuery.expr[':'].contains = function (a, i, m) {
    return jQuery(a).text().toUpperCase()
        .indexOf(m[3].toUpperCase()) >= 0;
}; // we are replacing the native jQuery contains filter with a case-insensitive alternative
// from: https://stackoverflow.com/questions/8746882/jquery-contains-selector-uppercase-and-lower-case-issue

function scrollToRow(value, type) {
    let row;
    let sf_suffix;
    if (type === 'table') {
        row = $('#data-table tr:contains(' + value.trim() + ')');
        console.log('#data-table tr:contains(' + value.trim() + ')')
        console.log(row)
        sf_suffix = 'tb'
    } else if (type === 'choices') {
        row = $('#choices li:contains(' + value.trim() + ')');
        sf_suffix = 'ch'
    }

    if (row.length > 0) {
        sf = $('#search-failure-'+sf_suffix)
        if (!sf.hasClass("invisible")) {
            sf.addClass("invisible");
        }
        row.addClass("highlight");
        setTimeout(function () {
            row.removeClass("highlight");
        }, 2000);
        row[0].scrollIntoView({ // row[0] gets the element rather than the query
            behavior: 'smooth',
            block: 'center'
        });
    } else {
        $('#search-failure-'+sf_suffix).removeClass('invisible')
    }
}