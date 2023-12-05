$(document).ready(function() {

    var searchBtn = $('search-btn');
    var searchForm = $('search-form');

    $(searchBtn).on('click', function() {
        searchForm.submit();
});
});