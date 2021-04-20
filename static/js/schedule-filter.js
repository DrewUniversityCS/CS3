document.querySelectorAll('.js_session_filter').forEach(item => {
  item.addEventListener('change', event => {
      console.log('Hello')
    document.querySelectorAll(`.js_section_${event.target.id}`).forEach(item => {
        item.style.display = event.target.checked ? 'block' : 'none'
    })
  })
})
