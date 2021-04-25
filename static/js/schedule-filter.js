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