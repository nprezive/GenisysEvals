Better Data Table
---
Features:
  * Responsive (changes design when width is smaller than 600px to best accommodate small screens)
  * Filter (by all columns or by one column)
  * Ajax call support
  * Sorting by columns
  * Cell formatter methods
  * Cell component renderer (through Vue scoped slots)
  * Pagination
  * Columns picker
  * Row selection (single or multiple)

## Basic Usage

.html
``` html
<better-data-table
  :rows="table"
  :config="config"
  :columns="columns"
  :ajaxCall="ajaxCall"
  @rowclick="rowclick"
  ref="mytable"
>
  <!-- Custom renderer for "source" column -->
  <template slot="msg" scope="cell">
    <span>
      {{ cell.data }}
      <q-tooltip>{{ cell.data}}</q-tooltip>
    </span>
  </template>

  <!-- Custom renderer when user selected one or more rows -->
  <template slot="selection" scope="selection">
    <q-btn color="primary" @click="changeMessage(selection)">
      <i>edit</i>
    </q-btn>
    <q-btn color="primary" @click="deleteRow(selection)">
      <i>delete</i>
    </q-btn>
  </template>
</better-data-table>
```
.js
``` js
// configuration properties
config: {
  title: 'Table Title',
  header: true,
  columnPicker: true,
  ajaxSearch: true,
  bodyStyle: {
    height: '300px'
  },
  rowHeight: '55px',
  pagination: {
    itemCount: 0,
    rowsPerPage: 5,
    options: [2, 5, 10, 15]
  },
  selection: 'multiple',
  messages: {
    noData: '<i>warning</i> No data available to show.',
    noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
  }
},
columns: [
  {
    label: 'ID',
    field: 'id',
    sort: true,
    type: 'string'
  },
  {
    label: 'Message',
    field: 'msg',
    type: 'template'
  }
],
table: [
  {
    id: 1,
    date: '21-10-2016',
    msg: 'Some message',
  },
  {
    id: 2,
    date: '22-11-2017',
    msg: 'Some other message'

  },
  ...
],

// functions
ajaxCall (searchTerm, page, rowsPerPage, ordering) {

  //example of how to force spinner on for an ajax call using refs
  this.$refs.mytable.tableSpinner = true
  
  this.$http({
    method: 'get',
    url: '/api/somecall/' + '?search=' + searchTerm + '&page=' + page + '&page_size=' + rowsPerPage '&ordering=' + ordering,
    headers: {}
  }).then(response => {
    if (response.status === 250) {
      this.$router.error = response.data
      this.$router.push({path: '/error'})
    }
    this.config.pagination.itemCount = response.data.count
    this.rows = response.data.results
    
    //example of how to force spinner off for an ajax call using refs
    this.$refs.mytable.tableSpinner = false
    
  }).catch(error => {
    console.log(error)
  })
},
rowclick (row) {
  console.log(row)
}
```

## Vue Properties
All Vue properties are **required**.

| Vue Property | Description |
| --- | --- |
| `config` | Config object (see "Config Property" below). |
| `columns` | Object defining columns (see "Columns Definition" below). |
| `rows` | Data containing Array of rows to display. |
| `ajaxCall` | Triggered when user types in search bar, changes pages, or rows per page (when ajaxSearch = true). Function format: ajaxCall(searchTerm, page, rowsPerPage) and must set rows and pagination.itemCount in promise/response|
| `rowClick` | Triggered when user clicks on a row. |

### Config Property
Below is an example enabling all features:

``` js
config = {
  // [REQUIRED] Set the row height
  rowHeight: '50px',
  
  // (optional) Title to display
  title: 'Data Table',
  
  // (optional) Columns header
  header: true,
  
  // (optional)
  // User will be able to choose which columns should be displayed
  columnPicker: true,
  
  // (optional)
  // Styling the body of the data table;
  // "minHeight", "maxHeight" or "height" are important
  bodyStyle: {
    maxHeight: '500px'
  },
  
  // (optional)
  // Enable ajax search when entering in search bar, parent handles
  // all ajax calls and must update the rows property and the pagination.itemCount
  // see .js ajaxCall() function example above
  ajaxSearch: false,
  
  // (optional) Use pagination. Set how many rows per page
  // and also specify an additional optional parameter ("options")
  // which forces user to make a selection of how many rows per
  // page he wants from a specific list
  // *** if ajaxSearch is used, item count must be updated by parent to let
  // child know how many items are in the list
  pagination: {
    itemCount: 0
    rowsPerPage: 15,
    options: [5, 10, 15, 30, 50, 500]
  },
  
  // (optional) Select one or more rows for an action
  // "single" adds a column with radio buttons for single row selection
  // "multiple" adds a column with checkboxes for multiple row selection
  // omitting the property will result in no selection column at all
  // if selection is included, a custom slotted template must also be used
  selection: 'multiple',
  
  // (optional) Override default messages when no data is available
  // or the user filtering returned no results.
  messages: {
    noData: '<i>warning</i> No data available to show.',
    noDataAfterFiltering: '<i>warning</i> No results. Please refine your search terms.'
  }
}
```

### Columns definition
``` js
columns = [
  {
    // [REQUIRED] Column name
    label: 'Date',
    
    // [REQUIRED] Row property name
    field: 'isodate',
    
    // (optional) Sortable column?
    sort: true
    
    // (optional) Column CSS style
    style: {color: '#ff09fa'},
    
    // (optional) Column CSS classes
    classes: 'bg-primary',
    // "classes" can be an array also ['bg-primary', 'text-white']
    
    // [REQUIRED] Row property type
    // Available values: "template", "html", "string", "number", "boolean"
    type: 'string',
    
    // (optional) Format column return data, **type MUST BE string**.
    //Access to value and row, must return a string
    format (value, row) {
      return value.from
    }
  },
  ...
]
```

#### Formatting a Cell using Rendering with Component
Sometimes you need to use a Tooltip or some specific component to render the cell. You can define a Vue component through a scoped slot:

``` html
<better-data-table ...>
  <!-- Custom renderer for "message" column -->
  <template slot="col-message" scope="cell">
    <span class="light-paragraph">{{cell.data}}</span>
  </template>
</better-data-table>
```

The `scope` property here (named `cell`) is an Object containing:

| Scope Property | Description |
| --- | --- |
| `row` | Object containing the row of the respective cell. |
| `col` | Object containing column definition for the respective cell. |
| `data` | Cell value. |

> Slot attribute must have a value of the following form: `[field_name]`.
Examples: "msg" (for field "msg"), "date" (for field "date").

A field is a property name of a row. Example of Data Table `table` Vue property (which is an Array of all rows):
``` js
table = [
  {
    id: 1,
    date: '21-10-2016',
    msg: 'Some message',
    ...
  },
  ...
]
```
