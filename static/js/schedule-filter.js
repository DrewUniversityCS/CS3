const params = new URLSearchParams(window.location.search)
var showSections = params.get('showsections') ? params.get('showsections').split(',') : []

for(var i=0; i<showSections.length; i++) {
    if(showSections[i]) {
        var sectionFilter = document.getElementById(showSections[i]);
        sectionFilter.checked = false;
        document.querySelectorAll(`.js_section_${showSections[i]}`).forEach(item => {
            item.style.display = 'none';
        })
    }
}


document.getElementById('js_clear_all_btn').addEventListener('click', event => {
    var boxes = document.querySelectorAll('.js_session_filter');
    var is_all_checked = true;
    for(i=0; i< boxes.length; i++) {
        is_all_checked = is_all_checked && boxes[i].checked;
    }

    for(i=0; i< boxes.length; i++) {
        if(is_all_checked){
            boxes[i].checked=false;
            document.querySelectorAll(`.js_section_${boxes[i].id}`).forEach(item => {
                item.style.display = 'none';
            })
        }
        else{
            boxes[i].checked=true;
            document.querySelectorAll(`.js_section_${boxes[i].id}`).forEach(item => {
                item.style.display = 'block';
            })
        }
    }
    var sections = document.querySelectorAll('.js_session_filter');
    var i;
    var str=[];
    for(i=0; i<sections.length; i++) {
        if(!sections[i].checked){
            str.push(sections[i].id)
        }
    }
    history.pushState({}, '', '?showsections='+str.toString())

  })


document.querySelectorAll('.js_session_filter').forEach(item => {
  item.addEventListener('change', event => {
    document.querySelectorAll(`.js_section_${event.target.id}`).forEach(item => {
        item.style.display = event.target.checked ? 'block' : 'none';
    })
    var sections = document.querySelectorAll('.js_session_filter');
    var i;
    var str=[];

    for(i=0; i<sections.length; i++) {

        if(!sections[i].checked){
            str.push(sections[i].id)
        }
    }
    history.pushState({}, '', '?showsections='+str.toString())
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

function CreateSectionNote(event, url, color_note_list_selector, color_dot_list_selector) {
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
            var formDivs = document.getElementsByClassName(color_note_list_selector.replace('<<color_type>>', obj['color'].slice(1)))
            // check if the divs exists, if not make them

            if (formDivs.length){
                for(i=0; i<formDivs.length; i++) {
                    formDivs[i].innerHTML = restext;
                }
            }
            else{
                var dotDivChilds = document.getElementsByClassName(color_dot_list_selector)
                for(i=0; i<dotDivChilds.length; i++) {
                    dotDivChilds[i].innerHTML = `${dotDivChilds[i].innerHTML}<div class="${color_note_list_selector.replace('<<color_type>>', obj['color'].slice(1))}">${restext}</div>`
                }
            }
            event.target.reset();
        }
    );
}

function editSection(e) {
    console.log(e);
    e.preventDefault();
    console.log(e.target.action+window.location.search)
    e.target.action = e.target.action+window.location.search
    e.target.submit()
}
