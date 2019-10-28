data = [{
  "name": "bootstrap-table",
  "commits": "10",
  "attention": "122",
  "url": "https://www.digitec.ch/"
},
 {
  "name": "multiple-select",
  "commits": "288",
  "attention": "20",
  "url": "https://www.digitec.ch/"
}, {
  "name": "Testing",
  "commits": "340",
  "attention": "20",
  "url": "https://www.digitec.ch/"
}]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
  {
    "field": "name", # which is the field's name of data key
    "title": "name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "commits",
    "title": "commits",
    "sortable": True,
  },
  {
    "field": "attention",
    "title": "attention",
    "sortable": True,
  },
  {
    "field": "url",
    "title": "url",
    "sortable": True,
  }
]
