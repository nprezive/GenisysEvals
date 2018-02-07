import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

function load (component) {
  // '@' is aliased to src/components
  return () => System.import(`@/${component}.vue`)
}

export default new VueRouter({
  /*
   * NOTE! VueRouter "history" mode DOESN'T works for Cordova builds,
   * it is only to be used only for websites.
   *
   * If you decide to go with "history" mode, please also open /config/index.js
   * and set "build.publicPath" to something other than an empty string.
   * Example: '/' instead of current ''
   *
   * If switching back to default "hash" mode, don't forget to set the
   * build publicPath back to '' so Cordova builds work again.
   */

  routes: [
    {
      path: '/',
      component: load('containers/Dashboard'),
      redirect: '/login',
      children: [
        {
          path: 'dashboard',
          name: 'tempDashboard',
          component: load('views/tempDashboard')
        },
        {
          path: 'charts',
          name: 'Charts',
          component: load('views/Charts')
        },
        {
          path: 'courses',
          name: 'Courses',
          component: load('containers/Courses'),
          children: [
            {
              path: '/',
              name: 'My Courses',
              component: load('views/Courses')
            }
          ]
        },
        {
          path: 'exams',
          name: 'Manage Exam',
          component: load('containers/ManageExam'),
          children: [
            {
              path: ':id',
              name: 'Manage An Exam',
              component: load('views/ManageExam'),
              props: true
            }
          ]
        },
        {
          path: 'proctoring',
          name: 'Proctoring',
          component: load('views/Proctoring')
        },
        {
          path: 'results',
          name: 'Results',
          component: load('views/Results')
        },
        {
          path: 'checkin',
          name: 'Checkin',
          component: load('containers/Checkin')
        },
        {
          path: 'evals',
          name: 'Evaluation',
          component: load('views/Evaluations')
        },
        {
          path: 'library',
          name: 'Library',
          component: load('containers/Library'),
          children: [
            {
              path: '/',
              name: 'My Library',
              component: load('views/library/LibraryBrowse'),
              props: true
            },
            {
              path: 'exam/:id',
              name: 'Manage Exam',
              component: load('views/ManageExam'),
              props: true
            }
          ]
        },
        {
          path: 'components',
          redirect: '/components/buttons',
          name: 'Components',
          component: {
            render (c) {
              return c('router-view')
            }
          },
          children: [
            {
              path: 'buttons',
              name: 'Buttons',
              component: load('views/components/Buttons')
            },
            {
              path: 'social-buttons',
              name: 'Social Buttons',
              component: load('views/components/SocialButtons')
            },
            {
              path: 'cards',
              name: 'Cards',
              component: load('views/components/Cards')
            },
            {
              path: 'forms',
              name: 'Forms',
              component: load('views/components/Forms')
            },
            {
              path: 'modals',
              name: 'Modals',
              component: load('views/components/Modals')
            },
            {
              path: 'switches',
              name: 'Switches',
              component: load('views/components/Switches')
            },
            {
              path: 'tables',
              name: 'Tables',
              component: load('views/components/Tables')
            }
          ]
        },
        {
          path: 'icons',
          redirect: '/icons/font-awesome',
          name: 'Icons',
          component: {
            render (c) {
              return c('router-view')
            }
          },
          children: [
            {
              path: 'font-awesome',
              name: 'Font Awesome',
              component: load('views/icons/FontAwesome')
            },
            {
              path: 'glyphicons',
              name: 'Glyphicons',
              component: load('views/icons/Glyphicons')
            },
            {
              path: 'glyphicons-filetypes',
              name: 'Glyphicons Filetypes',
              component: load('views/icons/GlyphiconsFiletypes')
            },
            {
              path: 'glyphicons-social',
              name: 'Glyphicons Social',
              component: load('views/icons/GlyphiconsSocial')
            },
            {
              path: 'simple-line-icons',
              name: 'Simple Line Icons',
              component: load('views/icons/SimpleLineIcons')
            }
          ]
        }
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: load('views/Login')
    },
    {
      path: '/blanktemplate',
      name: 'Blank Template',
      component: load('views/BlankTemplate')
    },
    {
      path: '/takeexam',
      name: 'TakeExam',
      component: load('containers/TakeExam'),
      children: [
        {
          path: 'start/:id',
          name: 'Start Exam',
          component: load('views/takeexam/StartTakeExam'),
          props: true
        },
        {
          path: 'exam/:id',
          name: 'Exam',
          component: load('views/takeexam/TakeExam'),
          props: true
        },
        {
          path: 'error',
          name: 'Unable Take Exam',
          component: load('views/takeexam/UnableTakeExam'),
          props: true
        },
        {
          path: 'end/:id',
          name: 'End Exam',
          component: load('views/takeexam/EndExam'),
          props: true
        },
        {
          path: 'review/:id',
          name: 'Review Exam',
          component: load('views/review/ReviewExam'),
          props: true
        }
      ]
    },
    {
      path: '/review/:id',
      name: 'Review Result',
      component: load('views/review/ReviewResult')
    },
    {
      path: '/sendfinalgrades',
      name: 'SendFinalGrades',
      component: load('views/SendFinalGrades')
    },
    {
      path: '/error',
      name: 'Error',
      component: load('views/Error'),
      props: true
    },

    // Always leave this last one
    {path: '*', component: load('Error404')} // Not found
  ]
})
