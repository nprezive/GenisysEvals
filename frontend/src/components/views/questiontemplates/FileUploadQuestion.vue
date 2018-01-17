<template>
  <div class="row">
    <q-input class="col-12" type="textarea" :min-rows="7" :max-height="300" v-model="question.text"
             float-label="Question Text"></q-input>
    <div class="col-xl-3 col-lg-4 col-md-4 col-sm-6 col-xs-6">
      <q-input v-model="question.weight" type="number" :min="0"
               float-label="Question Weight"></q-input>
    </div>
    <div class="row col-xl-4 col-lg-6 col-md-6 col-sm-6 col-xs-6">
      <div class="col-xl-10 col-lg-10 col-md-10 col-sm-12 col-xs-12 ml-auto mr-auto">
        <q-select
          v-model="question.question_type_id"
          float-label="Question Type"
          :options="questiontypes"
          @change="typeChange(question.question_type_id, 7)"
        ></q-select>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'FileUploadQuestion',
    props: ['question', 'questiontypes', 'typeChange']
  }
</script>
