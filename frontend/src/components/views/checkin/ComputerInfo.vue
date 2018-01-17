<template>
  <div class="ComputerInfo m-3">
    <div class="row">
      <img class="ml-auto mr-auto" :src="station.user.picture_id">
    </div>
    <div class="row">
      <h3 class="col-12 text-center">{{ station.user.first_name }} {{ station.last_name }}</h3>
    </div>
    <div class="row">
      <h5 class="col-12 text-center">{{ station.examname }}</h5>
    </div>
    <table class="q-table striped-even loose highlight container">
      <thead>
      <tr>
        <th class="text-center">Instructor<span v-if="station.instructors.length > 1">s</span></th>
        <th class="text-center">Time Spent</th>
        <th class="text-center">Questions</th>
      </tr>
      </thead>
      <tbody>
      <tr class="cursor-pointer">
        <td class="text-center">
          <span v-for="(instructor, index) in station.instructors">
            <span>{{ instructor.first_name }} {{ instructor.last_name }}</span><span
            v-if="index + 2 < station.instructors.length">, </span><span
            v-if="index === station.instructors.length - 2">, and </span></span>
        </td>
        <td class="text-center">
          <span v-if="station.duration > 60">{{ Math.floor(station.duration / 60) }}H -</span>
          <span>{{ Math.floor(station.duration % 60) }}M - {{ Math.floor((station.duration - (Math.floor(station.duration / 60) * 60) - Math.floor(station.duration % 60)) * 60) }}S</span> /
          <span v-if="station.timelimit">{{ station.timelimit }}</span><span v-else>No Limit</span>
        </td>
        <td class="text-center">{{ station.questionscompleted }} / {{ station.totalquestions }}</td>
      </tr>
      </tbody>
    </table>
    <div class="row mt-3">
      <q-progress
        :percentage="station.questionscompleted / station.totalquestions * 100"
        v-show="true"
        class="col-8 ml-auto mr-auto"
        style="padding: 0;"
      ></q-progress>
    </div>
  </div>
</template>
<script>

  export default {
    name: 'ComputerInfo',
    props: {
      station: {
        type: Object,
        required: true
      }
    }
  }
</script>
<style lang="stylus">
</style>
