<template>
  <div  class="animated fadeIn">
    <div class="row">
      <div class="col-12">
        <b-tabs class="clearfix">
          <b-tab title="Reports">
            <div class="card-columns cols-2">
              <div class="card">
                <div class="card-header">
                  Line Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <line-example></line-example>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-header">
                  Bar Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <bar-example></bar-example>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-header">
                  Doughnut Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <doughnut-example></doughnut-example>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-header">
                  Radar Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <radar-example></radar-example>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-header">
                  Pie Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <pie-example></pie-example>
                  </div>
                </div>
              </div>
              <div class="card">
                <div class="card-header">
                  Polar Area Chart
                  <div class="card-actions">
                  <a href="http://www.chartjs.org"><small class="text-muted">docs</small></a>
                </div>
                </div>
                <div class="card-block">
                  <div class="chart-wrapper">
                    <polar-area-example></polar-area-example>
                  </div>
                </div>
              </div>
            </div>
          </b-tab>
          <b-tab title="Results" v-if="isResults">
            <p>Results</p>
          </b-tab>
        </b-tabs>
      </div>
    </div>
  </div>
</template>

<script>
  import BarExample from './charts/BarExample'
  import LineExample from './charts/LineExample'
  import DoughnutExample from './charts/DoughnutExample'
  import RadarExample from './charts/RadarExample'
  import PieExample from './charts/PieExample'
  import PolarAreaExample from './charts/PolarAreaExample'

  export default {
    name: 'charts',
    components: {
      BarExample,
      LineExample,
      DoughnutExample,
      RadarExample,
      PieExample,
      PolarAreaExample
    },
    computed: {
      isResults () {
        // Function Call to check if is teacher
        const isNotResults = false
        if (isNotResults) {
          return false
        }
        return true
      }
    }
  }
</script>
