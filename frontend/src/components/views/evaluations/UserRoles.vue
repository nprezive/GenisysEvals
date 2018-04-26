<template>
    <q-page padding>
        <!-- can add :filter-method to add filter by method -->
        <q-card>
            <q-card-main>
                <div class="row" style="border-bottom: 1px solid lightgrey;">
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <p> </p>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <h5>Faculty Member</h5>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <h5>Viewing Rights</h5>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <h5>Viewing Areas</h5>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <h5> </h5>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <p> </p>
                    </div>
                </div>
                <div class="row" v-for="fac in facArray" :key="fac.id" style="border-bottom: 1px solid lightgrey; padding:10px">
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2">
                        <p> <!-- padding --></p>
                    </div>
                    <div class="col-lg-2 col-md-2 col-sm-2 col-xs-2" style="font-size: 16px">
                        <p>{{ fac.name }}</p>
                    </div>
                    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1" style="font-size: 16px">
                        <q-select
                          v-model="fac.level"
                          :options="options"
                          @change="checksaved(fac.id)"/>
                    </div>
                    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
                    </div>
                    <div v-if="fac.level != 'Own'" class="col-lg-1 col-md-1 col-sm-1 col-xs-1">
                        <q-list highlight>
                            <q-item v-for="area in FilterArea(fac.id)" :key="area.id">
                                <q-item-main>
                                    {{ area.name }}
                                </q-item-main>
                                <q-item-side right><q-btn round color="negative" @click="RemoveArea(fac.id, area)" small>X</q-btn> </q-item-side>
                            </q-item>
                            <q-item>
                                <q-item-main>
                                    <q-select
                                        v-model="fac.newArea"
                                        :options="computedAreas(fac.id)"
                                        @change="AddArea(fac.id)"/>
                                </q-item-main>
                            </q-item>
                        </q-list>
                    </div>
                    <div v-else class="col-lg-1 col-md-1 col-sm-1 col-xs-1" style="background-color: lightgrey; text-align: center; color: darkgrey; padding: 5px">
                        <p>Faculty can only see their own evaluations</p>
                    </div>
                    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 clearfix">
                            <p></p>
                    </div>
                    <div class="col-lg-1 col-md-1 col-sm-1 col-xs-1 clearfix">
                        <q-btn v-if="fac.changed" @click="PackageUp(fac.id)" color="primary">Update</q-btn>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-3 col-xs-3">
                        <p> <!-- padding --></p>
                    </div>
                </div>
            </q-card-main>
        </q-card>
    </q-page>
</template>

<script>
export default {
  data () {
    return {
      faculty: [
        {
          "id": 1,
          "name": "Brad Peterson",
          "level": "Adjunct",
          "changed": 0,
          "areas": [
            {
              "id": 1,
              "name": "CS"
            },
            {
              "id": 2,
              "name": "WEB"
            }
          ]
        },
        {
          "id": 2,
          "name": "Rich Fry",
          "level": "Department",
          "changed": 0,
          "areas": [
            {
              "id": 1,
              "name": "CS"
            },
            {
              "id": 2,
              "name": "WEB"
            },
            {
              "id": 3,
              "name": "NTM"
            }
          ]
        }
      ],
      areas: [
        {
          "id": 1,
          "name": "CS"
        },
        {
          "id": 2,
          "name": "WEB"
        },
        {
          "id": 3,
          "name": "NTM"
        },
        {
          "id": 4,
          "name": "NET"
        }
      ],
      areaArray: [],
      facArray: [],
      packageArray: [],
      currentKey: 1,
      options: [
        {
          label: 'Own',
          value: 'Own'
        },
        {
          label: 'Adjunct',
          value: 'Adjunct'
        },
        {
          label: 'Department',
          value: 'Department'
        }
      ]
    }
  },
  mounted: function () {
    this.$nextTick(function () {
      for (var i = 0; i < this.faculty.length; i++) {
        var newFac = {'id': this.faculty[i].id, 'name': this.faculty[i].name, 'level': this.faculty[i].level, 'changed': 0, 'newArea': ''}
        this.facArray.push(newFac)
        for (var j = 0; j < this.faculty[i].areas.length; j++) {
          var newArea = {'id': this.currentKey, 'facId': this.faculty[i].id, 'areaId': this.faculty[i].areas[j].id, 'name': this.faculty[i].areas[j].name, 'newArea': ''}
          this.areaArray.push(newArea)
          this.currentKey = this.currentKey + 1
        }
      }
    })
  },
  methods: {
    FilterArea: function (id) {
      let areas = this.areaArray
      areas = areas.filter((area) => {
        return area.facId === id
      })
      return areas
    },
    SpliceArea: function (area) {
      this.areaArray.splice(this.areaArray.indexOf(area), 1)
    },
    RemoveAllAreas: function (id) {
      let areas = this.areaArray
      areas = areas.filter((area) => {
        return area.facId === id
      })
      for (var i = 0; i < areas.length; i++) {
        this.SpliceArea(areas[i])
      }
    },
    RemoveArea: function (id, area) {
      let faculties = this.facArray
      faculties = faculties.filter((faculty) => {
        return faculty.id === id
      })
      this.FacultyUpdated(faculties)
      this.SpliceArea(area)
    },
    AddArea: function (id) {
      // this function adds a new area tied to faculty member and stores it in the areaArray
      let faculties = this.facArray
      faculties = faculties.filter((faculty) => {
        return faculty.id === id
      })
      var value = faculties[0].newArea && faculties[0].newArea.trim()
      if (value) {
        var areas = this.areas
        areas = areas.filter((area) => {
          return area.name === value
        })
        if (areas.length !== 0) {
          this.FacultyUpdated(faculties)
          var currentAreas = this.areaArray
          currentAreas = currentAreas.filter((area) => {
            return area.name === value && area.facId === id
          })
          if (currentAreas.length === 0) {
            var nArea = {'id': this.currentKey++, 'facId': id, 'areaId': areas[0].id, 'name': areas[0].name}
            this.areaArray.push(nArea)
          }
        }
      }
      faculties[0].newArea = ''
    },
    PackageUp: function (id) {
      // this function will get passed in faculty id and will package up their information to be sent to backend
      let areas = this.areaArray
      areas = areas.filter((area) => {
        return area.facId === id
      })
      let faculty = this.facArray
      faculty = faculty.filter((fac) => {
        return fac.id === id
      })
      if (faculty[0].level === 'Own') {
        // Remove all areas from faculty member
        this.RemoveAllAreas(faculty[0].id)
        areas = []
      }
      faculty[0].changed = 0
      var facAreas = []
      for (var i = 0; i < areas.length; i++) {
        facAreas.push({id: areas[i].areaId, name: areas[i].name})
      }
      var updatedFacInfo = {id: faculty[0].id, name: faculty[0].name, level: faculty[0].level, areas: facAreas}
      this.packageArray = updatedFacInfo
    },
    FacultyUpdated: function (faculties) {
      let faculty = faculties
      faculty[0].changed = 1
    },
    checksaved: function (id) {
      let faculties = this.facArray
      faculties = faculties.filter((fac) => {
        return fac.id === id
      })
      this.FacultyUpdated(faculties)
    },
    computedAreas: function (id) {
      let areas = []
      let faculty = this.areaArray
      faculty = faculty.filter((fac) => {
        return fac.facId === id
      })
      let found = true
      for (var i = 0; i < this.areas.length; i++) {
        found = true
        for (var j = 0; j < faculty.length; j++) {
          if (faculty[j].name === this.areas[i].name) {
            found = false
            break
          }
        }
        if (found) {
          // areas.push({'id': this.areas[i].id, 'name': this.areas[i].name})
          areas.push({'label': this.areas[i].name, 'value': this.areas[i].name})
        }
      }
      return areas
    }
  }
}
</script>
