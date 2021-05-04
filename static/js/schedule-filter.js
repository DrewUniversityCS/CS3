document.querySelectorAll('.js_session_filter').forEach(item => {
  item.addEventListener('change', event => {
    document.querySelectorAll(`.js_section_${event.target.id}`).forEach(item => {
        item.style.display = event.target.checked ? 'block' : 'none'
    })
  })
})

function loadEditForm(url, selector) {
    var formDivs = document.querySelectorAll(selector)
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

function loadSectionNoteCreateForm(url, selector) {
    var formDivs = document.querySelectorAll(selector)
    console.log(formDivs);
    if (formDivs[0].firstChild.tagName == 'IMG' ) {
        fetch(url).then(response => response.text()).then(data => {
            formDivs.forEach(item => {
                item.innerHTML = data;
            })
        });
    }
}

function CreateSectionNote(event, url, color_note_list_selector) {
    event.preventDefault();
    var elements = event.target.elements;
    var obj ={};
    for(var i = 0 ; i < elements.length ; i++){
        var item = elements.item(i);
        obj[item.name] = item.value;
    }
    console.log(document.getElementsByName('csrfmiddlewaretoken')[0].value)
    fetch(url, {
        method: 'post',
        body: JSON.stringify(obj),
        headers: new Headers({"X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value, 'content-type': 'application/json'}),
    })
    .then(res=> res.text())
    .then(restext => {
            event.target.parentNode.style.display = 'none';
            console.log(restext);
            var formDivs = document.querySelectorAll(color_note_list_selector.replace('<<color_type>>', obj['color']))
            formDivs.forEach(item => {
                item.innerHTML = restext;
            })
            event.target.reset();
        }
    );
}
