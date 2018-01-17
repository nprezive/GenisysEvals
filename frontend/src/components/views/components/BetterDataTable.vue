<template>
  <div class="wrapper relative-position">
    <div id="custom-data-table">
      <div class="row">
        <div class="col-12 custom-table-selection"
             v-if="(config.selection === 'multiple' && selection.length > 0) || (config.selection === 'single' && selection !== '')">
          <div class="row items-center" style="min-height: 38px">
            <span small class="col-2 items-span pl-2">
              <span v-if="selection.length > 0">{{ selection.length }}</span> item<span
              v-if="selection.length > 1">s</span> selected.
            </span>
            <q-btn class="col-1" small flat @click="clear">clear</q-btn>
            <div class="col-9 text-right">
              <slot name="selection" :props="selection">
              </slot>
            </div>
          </div>
        </div>
        <div class="col-12 custom-title-div" v-else>
          <div class="row">
            <div v-if="config.title" class="custom-title col pt-1 ellipsis">{{ config.title }}</div>
            <div v-else class="col"></div>
            <div class="row items-center" :style="{'margin-left': '35px'}">
              <div>
                <q-select
                  v-if="config.columnPicker"
                  multiple
                  toggle
                  display-value="Columns"
                  class="custom-columns-select"
                  v-model="columnsSelect"
                  :options="columnsOptions"
                ></q-select>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row custom-search-bar-row">
        <q-field class="col-12" v-if="!config.ajaxSearch">
          <q-search class="custom-search-bar pt-2" v-model="searchTerm" placeholder="Search" :debounce="0"
                    @change="search()">
          </q-search>
        </q-field>
        <q-field v-else :error="searchError" error-label="Please enter at least 3 characters" class="col-12">
          <q-search class="custom-ajax-search-bar pt-2" v-model="ajaxSearchTerm" placeholder="Search" :debounce="500"
                    @change="ajaxSearch()">
            <q-spinner-mat v-show="searchSpinner" color="tertiary" :size="24"></q-spinner-mat>
          </q-search>
        </q-field>
      </div>
      <div :style="config.bodyStyle" class="table-wrapper-div row">
        <table class="q-table highlight horizontal-separator striped-odd custom-table w-100 pt-2"
               :class="windowWidth < 601 ? 'responsive' : ''">
          <thead>
          <tr v-if="config.header">
            <th class="custom-table-heading cursor-pointer"
                v-if="config.selection === 'multiple' || config.selection === 'single'"></th>
            <th v-for="(column, cindex) in columns" :key="cindex"
                class="custom-table-heading cursor-pointer" v-if="hideColumn(column.label)">
              <q-icon v-if="column.sort" @click="sortColumn(column.field, cindex)"
                      :name="iconIndex === cindex ? iconName : 'import_export'"></q-icon>
              <span>{{ column.label }}</span>
              <q-tooltip>{{ column.label }}</q-tooltip>
            </th>
          </tr>
          </thead>
          <span v-if="config.ajaxSearch && !config.pagination">config.ajaxSearch and config.pagination options must both be set</span>
          <div v-if="currentRows.length === 0 && config.messages"
               class="custom-table-message q-data-table-message text-center mt-2">
            <span
              v-if="currentRows.length === 0 && (searchTerm.length > 0 || ajaxSearchTerm.length > 0) && config.messages.noDataAfterFiltering"
              v-html="config.messages.noDataAfterFiltering"></span>
            <span v-else-if="currentRows.length === 0 && config.messages.noData" v-html="config.messages.noData"></span>
          </div>
          <tbody>
          <tr class="custom-table-row cursor-pointer" :style="windowWidth > 600 ? {height: config.rowHeight} : {}"
              v-for="(row, rindex) in currentRows" :key="rindex">
            <td v-if="config.selection === 'multiple' || config.selection === 'single'"
                class="custom-table-data custom-table-data-selection text-center"
                @click="toggleRowSelection(row)">
              <q-checkbox v-if="config.selection === 'multiple'" v-model="selection" :val="row"></q-checkbox>
              <q-radio v-if="config.selection === 'single'" v-model="selection" :val="row"></q-radio>
            </td>
            <td :data-th="column.label" class="custom-table-data" :class="column.classes" :style="windowWidth < 600 ? {'margin' : '5px'} : column.style"
                v-for="(column, cindex) in columns" :key="cindex" v-if="hideColumn(column.label)"
                @click="$emit('rowclick', row )">
              <div v-if="column.type === 'template'">
                <slot :name="column.field" :row="row" :column="column" :data="row[column.field]">
                </slot>
              </div>
              <div v-else-if="column.type === 'html'">
                <div v-html="row[column.field]"></div>
              </div>
              <div v-else-if="column.type === 'string'">
                <div v-if="column.format">
                  {{ column.format(row[column.field], row) }}
                </div>
                <div v-else>
                  {{ row[column.field] }}
                </div>
              </div>
              <div v-else-if="column.type === 'number'">
                {{ row[column.field] }}
              </div>
              <div v-else-if="column.type === 'boolean'">
                {{ row[column.field] }}
              </div>
              <div v-else>
                None
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <div v-if="config.ajaxSearch || config.pagination" class="text-right">
        <div class="inline-block">
          <span class="custom-rows-label">Rows</span>
        </div>
        <div class="inline-block pl-4 pr-4">
          <q-select
            class="custom-select-box"
            v-model="rowsPerPageSelect"
            :options="rowsPerPageOptions"
            :disable="searchError"
          ></q-select>
        </div>
        <div class="inline-block text-center">
          <div v-if="config.ajaxSearch && config.pagination" class="custom-current-page">
            {{ localPagination.firstVar }} - {{ localPagination.secondVar }} / {{ config.pagination.itemCount }}
          </div>
          <div v-else class="custom-current-page">
            {{ localPagination.firstVar }} - {{ localPagination.secondVar }} / {{ nonAjaxItemCount }}
          </div>
        </div>
        <div class="inline-block pl-4 pr-2">
          <q-pagination class="custom-pagination"
                        style="min-width: 165px !important;" v-model="currentPage"
                        :disable="searchError"
                        :max="localPagination.pages" v-if="config.pagination"></q-pagination>
        </div>
      </div>
      <q-inner-loading :visible="tableSpinner">
        <q-spinner-gears size="50px" color="primary"></q-spinner-gears>
      </q-inner-loading>
    </div>
  </div>
</template>

<script>

  import _ from 'lodash'

  export default {
    name: 'CustomDataTable',
    props: ['rows', 'columns', 'config', 'ajaxCall'],
    data () {
      return {
        searchTerm: '',
        ajaxSearchTerm: '',
        searchError: false,
        searchSpinner: false,
        tableSpinner: false,
        eschewTableSpinner: false,
        currentPage: 1,
        localPagination: {
          firstVar: '',
          secondVar: '',
          pages: 1
        },
        nonAjaxItemCount: 0,
        columnsSelect: [],
        columnsOptions: [],
        rowsPerPageSelect: '0',
        rowsPerPageOptions: [],
        currentRows: false,
        iconIndex: 0,
        iconName: 'import_export',
        bodyStyle: {},
        selection: [],
        props: {},
        windowWidth: 0,
        windowHeight: 0,
        indexToSort: 0,
        columnToSort: '',
        ajaxColumnSort: ''
      }
    },
    mounted () {
      this.currentRows = []
      if (this.rows) {
        for (let i = 0; i < this.rows.length; i++) {
          this.currentRows.push(this.rows[i])
        }
      }
      if (this.config.selection) {
        if (this.config.selection.toString() === 'multiple') {
          this.selection = []
        } else if (this.config.selection.toString() === 'single') {
          this.selection = ''
        } else {
          this.selection = undefined
        }
      } else {
        this.selection = undefined
      }
      if (this.config.ajaxSearch) {
        if (!this.config.pagination) {
          this.currentRows = []
        }
      } else {
        this.nonAjaxItemCount = this.currentRows.length
      }
      if (this.columns) {
        for (let i = 0; i < this.columns.length; i++) {
          let obj = {
            label: this.columns[i].label,
            value: this.columns[i].label
          }
          this.columnsOptions.push(obj)
          this.columnsSelect.push(this.columns[i].label)
        }
      }
      if (this.config.pagination) {
        this.rowsPerPageSelect = this.config.pagination.rowsPerPage
        for (let i = 0; i < this.config.pagination.options.length; i++) {
          let obj = {
            label: this.config.pagination.options[i] + '',
            value: this.config.pagination.options[i]
          }
          this.rowsPerPageOptions.push(obj)
        }
        if (!this.config.ajaxSearch) {
          this.config.pagination.itemCount = this.currentRows.length
          this.setPagination(this.rowsPerPageSelect, this.currentPage, this.config.pagination.itemCount)
        }
      }
      this.$nextTick(function () {
        window.addEventListener('resize', this.getWindowWidth)
        window.addEventListener('resize', this.getWindowHeight)

        this.getWindowWidth()
        this.getWindowHeight()
      })
    },
    beforeDestroy () {
      window.removeEventListener('resize', this.getWindowWidth)
      window.removeEventListener('resize', this.getWindowHeight)
    },
    watch: {
      currentPage (newVal) {
        if (this.config.ajaxSearch) {
          if (this.eschewTableSpinner) {
            this.eschewTableSpinner = false
          } else {
            this.tableSpinner = true
          }
          this.ajaxCall(this.ajaxSearchTerm, newVal, this.rowsPerPageSelect, this.ajaxColumnSort)
        } else {
          this.filterSortPaginate()
        }
      },
      rowsPerPageSelect (newVal) {
        if (this.config.ajaxSearch) {
          if (this.currentPage === 1) {
            this.ajaxCall(this.ajaxSearchTerm, this.currentPage, newVal, this.ajaxColumnSort)
          } else {
            this.currentPage = 1
          }
        } else {
          if (this.currentPage === 1) {
            this.filterSortPaginate()
          } else {
            this.currentPage = 1
          }
        }
      },
      rows (newVal) {
        this.currentRows = []
        if (this.rows) {
          for (let i = 0; i < this.rows.length; i++) {
            this.currentRows.push(this.rows[i])
          }
        }
        if (this.config.ajaxSearch) {
          this.setPagination(this.rowsPerPageSelect, this.currentPage, this.config.pagination.itemCount)
          this.searchSpinner = false
          this.tableSpinner = false
        } else {
          if (this.config.pagination) {
            this.filterSortPaginate()
          }
        }
      }
    },
    methods: {
      propertyIn (object, term) {
        for (let item in object) {
          if (object.hasOwnProperty(item)) {
            if (typeof object[item] === 'object' && object[item] !== null) {
              return this.propertyIn(object[item], term)
            }
            if (object[item] !== null && object[item] !== '') {
              if (object[item].toString().toLowerCase().includes(term.toLowerCase())) {
                return true
              }
            }
          }
        }
        return false
      },
      filterSortPaginate () {
//        filter
        this.currentRows = []
        if (this.rows) {
          for (let i = 0; i < this.rows.length; i++) {
            this.currentRows.push(this.rows[i])
          }
        }
        let searchFilteredRows = []
        if (this.searchTerm.length > 0) {
          searchFilteredRows = this.currentRows.filter(item => {
            if (this.propertyIn(item, this.searchTerm)) {
              return item
            }
          })
        } else {
          searchFilteredRows = this.currentRows
        }
//        sort
        let unsortedRows = searchFilteredRows
        if (this.columnToSort !== '') {
          let that = this
          if (this.iconIndex === this.indexToSort) {
            if (this.iconName === 'import_export') {
              this.iconName = 'arrow_downward'
              searchFilteredRows.sort(function (a, b) {
                if (a[that.columnToSort] < b[that.columnToSort]) return -1
                if (a[that.columnToSort] > b[that.columnToSort]) return 1
                return 0
              })
            } else if (this.iconName === 'arrow_upward') {
              this.iconName = 'import_export'
              searchFilteredRows = unsortedRows
            } else if (this.iconName === 'arrow_downward') {
              this.iconName = 'arrow_upward'
              searchFilteredRows.sort(function (a, b) {
                if (a[that.columnToSort] > b[that.columnToSort]) return -1
                if (a[that.columnToSort] < b[that.columnToSort]) return 1
                return 0
              })
            } else {
              this.iconName = 'error'
            }
          } else {
            this.iconIndex = this.indexToSort
            this.iconName = 'arrow_downward'
            searchFilteredRows.sort(function (a, b) {
              if (a[that.columnToSort] < b[that.columnToSort]) return -1
              if (a[that.columnToSort] > b[that.columnToSort]) return 1
              return 0
            })
          }
        }
//        paginate
        let paginatedRows = []
        for (let i = (this.currentPage - 1) * parseInt(this.rowsPerPageSelect); i <= (this.currentPage * parseInt(this.rowsPerPageSelect)) - 1; i++) {
          if (searchFilteredRows[i] !== undefined) {
            paginatedRows.push(searchFilteredRows[i])
          }
        }
        if (this.searchTerm.length > 0) {
          this.nonAjaxItemCount = searchFilteredRows.length
          this.setPagination(this.rowsPerPageSelect, this.currentPage, this.nonAjaxItemCount)
        } else {
          this.nonAjaxItemCount = this.currentRows.length
          this.setPagination(this.rowsPerPageSelect, this.currentPage, this.currentRows.length)
        }
        this.currentRows = paginatedRows
      },
      sortColumn (column, index) {
        if (this.config.ajaxSearch) {
          if (this.iconIndex === index) {
            if (this.iconName === 'import_export') {
              this.iconName = 'arrow_downward'
              this.ajaxColumnSort = column
            } else if (this.iconName === 'arrow_upward') {
              this.iconName = 'import_export'
              this.ajaxColumnSort = ''
            } else if (this.iconName === 'arrow_downward') {
              this.iconName = 'arrow_upward'
              this.ajaxColumnSort = '-' + column
            } else {
              this.iconName = 'error'
            }
          } else {
            this.iconIndex = index
            this.iconName = 'arrow_downward'
            this.ajaxColumnSort = column
          }
          this.ajaxCall(this.ajaxSearchTerm, this.currentPage, this.rowsPerPageSelect, this.ajaxColumnSort)
        } else {
          this.columnToSort = column
          this.indexToSort = index
          this.filterSortPaginate()
        }
      },
      filterResults () {
        let searchFilteredRows = []
        if (this.searchTerm.length > 0) {
          searchFilteredRows = this.rows.filter(item => {
            return item.name.toLowerCase().indexOf(this.searchTerm.toLowerCase()) > -1
          })
        } else {
          searchFilteredRows = this.rows
        }
        this.currentRows = searchFilteredRows
      },
      search () {
        if (this.config.pagination) {
          if (this.currentPage === 1) {
            this.filterSortPaginate()
          } else {
            this.currentPage = 1
          }
        } else {
          this.filterResults()
        }
      },
      ajaxSearch () {
        if (this.ajaxSearchTerm.length > 2) {
          this.searchError = false
          this.searchSpinner = true
          if (this.currentPage === 1) {
            if (typeof this.ajaxCall === 'function') {
              this.ajaxCall(this.ajaxSearchTerm, this.currentPage, this.rowsPerPageSelect, this.ajaxColumnSort)
            }
          } else {
            this.eschewTableSpinner = true
            this.currentPage = 1
          }
        } else if (this.ajaxSearchTerm.length < 3 && this.ajaxSearchTerm.length > 0) {
          this.searchError = true
        } else if (this.ajaxSearchTerm.length === 0) {
          this.tableSpinner = true
          this.searchError = false
          if (this.currentPage === 1) {
            if (typeof this.ajaxCall === 'function') {
              this.ajaxCall(this.ajaxSearchTerm, this.currentPage, this.rowsPerPageSelect, this.ajaxColumnSort)
            }
          } else {
            this.currentPage = 1
          }
        }
      },
      setPagination (rowsPerPage, page, count) {
        this.localPagination.firstVar = (((page - 1) * rowsPerPage) + 1)
        this.localPagination.secondVar = (page * rowsPerPage)
        if (this.localPagination.secondVar > count) {
          this.localPagination.secondVar = count
        }
        this.localPagination.pages = Math.ceil(parseFloat(count / rowsPerPage))
        if (this.localPagination.pages === 0) {
          this.localPagination.pages = 1
        }
      },
      clear () {
        if (this.config.selection.toString() === 'multiple') {
          this.selection = []
        } else if (this.config.selection.toString() === 'single') {
          this.selection = ''
        } else {
          this.selection = undefined
        }
      },
      toggleRowSelection (row) {
        if (_.includes(this.selection, row)) {
          this.selection = _.reject(this.selection, row)
        } else {
          this.selection.push(row)
        }
      },
      hideColumn (label) {
        for (let i = 0; i < this.columnsSelect.length; i++) {
          if (label === this.columnsSelect[i]) {
            return true
          }
        }
        return false
      },
      getWindowWidth (event) {
        this.windowWidth = document.documentElement.clientWidth
      },

      getWindowHeight (event) {
        this.windowHeight = document.documentElement.clientHeight
      }
    }
  }
</script>
<style lang="stylus">

  #custom-data-table .custom-title-div
    padding: 8px 0 4px 0
    min-height: 50px
    .q-select
      margin: 0

  #custom-data-table .custom-table-selection
    padding: 6px 0 6px 0
    min-height: 50px
    color: #027be3
    background: rgba(2, 123, 227, 0.2)
    span.items-span
      font-size: 85%
      font-weight: 300

  #custom-data-table .custom-title
    font-weight: 300

  #custom-data-table .custom-columns-select
    font-weight: 300

  #custom-data-table .custom-search-bar-row .q-field
    margin-top: 0

  #custom-data-table .custom-ajax-search-bar input
    font-weight: 300

  #custom-data-table .custom-search-bar input
    font-weight: 300

  #custom-data-table .table-wrapper-div
    overflow: auto

  #custom-data-table .custom-table-heading
    border-bottom: 2px solid #bdbdbd !important

  #custom-data-table .custom-table-data-selection
    border-right: dotted lightgray 1px

  @media (max-width: 600px)
    #custom-data-table .custom-table-data
      font-size: 85%

  @media (min-width: 601px)
    #custom-data-table .custom-table-data
      border-bottom: 1px solid rgba(0, 0, 0, 0.12)
      font-size: 85%

  #custom-data-table .custom-table.q-table th
    color: rgba(0, 0, 0, 0.54)
    vertical-align: middle
    font-size: 85%

  #custom-data-table .custom-table-row
    width: 100%

  #custom-data-table .custom-select-box .q-input-target
    font-weight: 300

  #custom-data-table .custom-rows-label
    font-weight: 300
    font-size: 85%

  #custom-data-table .custom-current-page
    color: rgba(12, 12, 12, 0.6)
    font-size: 85%

  #custom-data-table .custom-pagination
    font-weight: 300

    input.q-input-target
      text-align: center !important

</style>
