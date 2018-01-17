<template>
  <div class="mt-3 mb-3">
    <q-list no-border separator link style="max-height: 50em; overflow-y: scroll;">
      <q-item v-for="(site, index) in sites" :key="index"
              @click="clickSite(site)"
              :class="{active: site.id === chosenSite}"
              v-if="site.siteCount > 0"
      >
        <q-item-side color="secondary" icon="fa-minus"></q-item-side>
        <q-item-main>
          <q-item-tile label class="font-sm">
            {{ site.name }}
          </q-item-tile>
          <q-item-tile sublabel class="font-xs">Site ID: {{ site.id }}</q-item-tile>
          <q-item-tile sublabel class="font-xs">Station Count: {{ site.siteCount }}</q-item-tile>
        </q-item-main>
      </q-item>
    </q-list>
  </div>
</template>

<script>
  export default {
    name: 'Sites',
    props: {
      sites: {
        type: Array,
        twoWay: true
      },
      clickSite: {
        type: Function
      },
      chosenSite: {
        type: Number
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .q-table
    border: none !important
</style>
