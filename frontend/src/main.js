// === DEFAULT / CUSTOM STYLE ===
// WARNING! always comment out ONE of the two require() calls below.
// 1. use next line to activate CUSTOM STYLE (./src/themes)
// require(`./themes/app.${__THEME}.styl`)
// 2. or, use next line to activate DEFAULT QUASAR STYLE
require(`quasar/dist/quasar.${__THEME}.css`)
// ==============================

// Uncomment the following lines if you need IE11/Edge support
require(`quasar/dist/quasar.ie`)
require(`quasar/dist/quasar.ie.${__THEME}.css`)

import Vue from 'vue'
// import Quasar from 'quasar'
import router from './router'
// import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import store from './store/index.js'

import Quasar, {
  QAutocomplete,
  QBtn,
  QCard,
  QCardActions,
  QCardMain,
  QCardSeparator,
  QCardTitle,
  QCarousel,
  QCheckbox,
  QChip,
  QCollapsible,
  QDataTable,
  QDatetime,
  QDatetimeRange,
  QDialogSelect,
  QFab,
  QFabAction,
  QField,
  QIcon,
  QInnerLoading,
  QInput,
  QItem,
  QItemMain,
  QItemSeparator,
  QItemSide,
  QItemTile,
  QLayout,
  QList,
  QListHeader,
  QModal,
  QModalLayout,
  QOptionGroup,
  QPagination,
  QPopover,
  QProgress,
  QRadio,
  QSearch,
  QSelect,
  QSideLink,
  QSlider,
  QSpinnerGears,
  QSpinnerHourglass,
  QSpinnerMat,
  QTab,
  QTabPane,
  QTabs,
  QToggle,
  QToolbar,
  QToolbarTitle,
  QTooltip,
  QUploader,
  QStepper,
  QStep,
  QStepperNavigation,
  QTree
} from 'quasar'

Vue.use(Quasar, {
  components: {
    QAutocomplete,
    QBtn,
    QCard,
    QCardActions,
    QCardMain,
    QCardSeparator,
    QCardTitle,
    QCarousel,
    QCheckbox,
    QChip,
    QCollapsible,
    QDataTable,
    QDatetime,
    QDatetimeRange,
    QDialogSelect,
    QFab,
    QFabAction,
    QField,
    QIcon,
    QInnerLoading,
    QInput,
    QItem,
    QItemMain,
    QItemSeparator,
    QItemSide,
    QItemTile,
    QLayout,
    QList,
    QListHeader,
    QModal,
    QModalLayout,
    QOptionGroup,
    QPagination,
    QPopover,
    QProgress,
    QRadio,
    QSearch,
    QSelect,
    QSideLink,
    QSlider,
    QSpinnerGears,
    QSpinnerHourglass,
    QSpinnerMat,
    QTab,
    QTabPane,
    QTabs,
    QToggle,
    QToolbar,
    QToolbarTitle,
    QTooltip,
    QUploader,
    QStepper,
    QStep,
    QStepperNavigation,
    QTree
  }
})

Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.use(Quasar) // Install Quasar Framework
// Vue.use(BootstrapVue)

if (__THEME === 'mat') {
  require('quasar-extras/roboto-font')
}
import 'quasar-extras/material-icons'
import 'quasar-extras/ionicons'
import 'quasar-extras/fontawesome'
import 'quasar-extras/animate'

Quasar.start(() => {
  /* eslint-disable no-new */
  new Vue({
    el: '#q-app',
    router,
    store,
    render: h => h(require('./App'))
  })
})

export const eventBus = new Vue({
  methods: {
    toggleSideNavSize () {
      this.$emit('toggleSize')
    },
    toggleSideNav () {
      this.$emit('toggle')
    },
    updateBreakpoint (payLoad) {
      this.$emit('updateBreakpoint', payLoad)
    }
  }
})
