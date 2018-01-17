<template>
  <ol id="breadcrumb" class="breadcrumb">
    <li class="breadcrumb-item" v-for="(item, index) in list" v-if="!isCourse(item, index)">
      <router-link :to="'/courses'" v-if="isFirst(index)">Home</router-link>
      <span class="active" v-else-if="isLast(index)">{{ showName(item, index) }}</span>
      <router-link :to="item.path" v-else>{{ showName(item) }}</router-link>
    </li>
  </ol>
</template>

<script>
  export default {
    name: 'Breadcrumb',
    props: {
      list: {
        type: Array,
        required: true,
        default: () => []
      },
      separator: String
    },
    methods: {
      isFirst (index) {
        return index === 0
      },
      isCourse (item, index) {
        if ((item.name === 'Courses' || item.name === 'Library') && !this.$router.cName) {
          return true
        }
        return false
      },
      isLast (index) {
        return index === this.list.length - 1
      },
      showName (item, index) {
        if (this.$router.cName && this.isLast(index)) {
          item = this.$router.cName
          this.$router.cName = false
        } else if (item.meta && item.meta.label) {
          item = item.meta && item.meta.label
        } else if (item.name) {
          item = item.name
        }
        return item
      }
    }
  }
</script>
