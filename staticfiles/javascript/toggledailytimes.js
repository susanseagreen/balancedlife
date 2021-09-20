function toggleDailyTimes() {
    if ($('#id_bool_daily').prop('checked')) {
        $('.open_close_block').hide()
    } else {
        $('.open_close_block').show()
    }
}