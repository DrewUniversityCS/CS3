// making sure no more than 8 are selceted as no one can take more thsn 2 courses
$("input:checkbox.js_subject_checkbox").click(function () {
    console.log($("input:checkbox:checked.js_subject_checkbox").length);
    var bol = $("input:checkbox:checked.js_subject_checkbox").length >= 2;
    $("input:checkbox.js_subject_checkbox").not(":checked").attr("disabled", bol);
});
