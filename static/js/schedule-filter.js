document.querySelectorAll('.js_session_filter').forEach(item => {
  item.addEventListener('change', event => {
    document.querySelectorAll(`.js_section_${event.target.id}`).forEach(item => {
        item.style.display = event.target.checked ? 'block' : 'none'
    })
  })
})

function loadEditForm(url, selector) {
    console.log('Being Called')
    var formDivs = document.querySelectorAll(selector)
    console.log(formDivs[0].firstChild.tagName)
    if (formDivs[0].firstChild.tagName == 'IMG' ) {
        fetch(url).then(response => response.text()).then(data => {
            formDivs.forEach(item => {
                item.innerHTML = data;
            })
        });
    }
}

function filterSectionCheckBoxes() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = li[i].id;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
